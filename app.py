import numpy as np
import pandas as pd
from PIL import Image
from io import BytesIO
import random, datetime, json, os
from collections import Counter, defaultdict
from flask import Flask, render_template, request, send_file, session
from utils.plotting import KeyHeatMap, Mappings, plot_kde, plot_placeholder

app=Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Define a route to serve the index.html file
@app.route('/')
def index():
    if 'KEY_DIST' not in session:
        session['KEY_DIST'] = Counter()
    if 'TIME_DATA' not in session:
        session['TIME_DATA'] = {}
    if 'SPEEDS' not in session:
        session['SPEEDS'] = []
    return render_template('index.html')


@app.route('/get_string', methods=['POST'])
def get_string():
    file_name = 'assets/naval-tweets.md' # text file with tweets seperated by ***
    with open(file_name, 'r') as file:
        data =  file.read()
        data = data.split('***')[1:]
    return random.choice(data).strip().replace('‘', "'").replace('’', "'").replace('“', '"').replace('”', '"')

@app.route('/save_data', methods=['POST'])
def save_data():
    data = request.get_json()

    current_datetime = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    speed = int(round(( len(data['inputString'])/5 ) / ( data['strokeTimes'][-1]/60000 )))
    
    filename = f'session_data/raw/typefase_{current_datetime}.json'
    with open(filename, 'w') as file:
        json.dump(data, file)
    
    df = pd.DataFrame({"datetime": [current_datetime], "speed": [speed]})
    isThere = os.path.exists("session_data/typing_speeds.csv"); mode = 'a' if isThere else 'w'
    df.to_csv("session_data/typing_speeds.csv", mode=mode, index=False, header=not isThere)

    # store typing speed for KDE
    session['SPEEDS'].append(speed)

    # store count data
    count = Counter(data['inputString'])
    session['KEY_DIST'] = Counter(session['KEY_DIST']) + count

   # get the average time for each key for the session
    map = Mappings()
    chars, times = [str(tuple(map.get_coord(each))) for each in data['inputString'][1:]], np.diff(data['outTimes'])
    session_data = defaultdict(lambda: {'average_time': 0, 'count': 0})
    for char, time in zip(chars, times):
        session_data[char]['count'] += 1
        session_data[char]['average_time'] += time
    for char in session_data:
        session_data[char]['average_time'] /= session_data[char]['count']

    # update the overall average time
    TIME_DATA = defaultdict(lambda: {'average_time': 0, 'count': 0}, session['TIME_DATA']); decay_factor=.1
    for char, data in session_data.items():
        TIME_DATA[char]['average_time'] = ((TIME_DATA[char]['average_time'] * TIME_DATA[char]['count']) + (data['average_time'] * data['count'])) / (TIME_DATA[char]['count'] + data['count'])
        TIME_DATA[char]['count'] += data['count']
    for char in TIME_DATA:
        TIME_DATA[char]['count'] *= (1 - decay_factor)
    session['TIME_DATA'] = TIME_DATA

    return '0'

@app.route('/get_image')
def get_image():
    kind = request.args.get('argument'); key_dict = {}
    if (kind=='count') & (len(session['KEY_DIST'])>0):
        map = Mappings()
        for k, v in session['KEY_DIST'].items():
            key = tuple(map.get_coord(k))
            key_dict[key] = key_dict.get(key, 0) + v
    
    elif (kind=='speed') & (len(session['TIME_DATA'])>0):
        key_dict = {eval(k):1000/v['average_time'] for k,v in session['TIME_DATA'].items()}

    khm = KeyHeatMap()
    byte_stream = khm.plot(key_dict)
    return send_file(byte_stream, mimetype='image/jpeg', as_attachment=True, download_name='image.jpg')

@app.route('/get_kde')
def get_kde():
    if len(session['SPEEDS'])>2:
        byte_stream = plot_kde(session['SPEEDS'])
    else:
        byte_stream = plot_placeholder()
    return send_file(byte_stream, mimetype='image/jpeg', as_attachment=True, download_name='image.jpg') 

if __name__ == '__main__':
    
    session_output_path = './session_data/raw'
    if not os.path.exists(session_output_path):
        os.makedirs(session_output_path, exist_ok=True)
    
    app.run(debug=False)
