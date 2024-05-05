import pandas as pd
from PIL import Image
from io import BytesIO
from collections import Counter
import random, datetime, json, os
from flask import Flask, render_template, request, send_file
from utils.plotting import KeyHeatMap

KEY_DIST = Counter()
app=Flask(__name__)

# Define a route to serve the index.html file
@app.route('/')
def index():
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
    filename = f'session_data/raw/typefase_{current_datetime}.json'
    with open(filename, 'w') as file:
        json.dump(data, file)
    
    df = pd.DataFrame({"datetime": [current_datetime], "speed": [int(round(( len(data['inputString'])/5 ) / ( data['strokeTimes'][-1]/60000 )))]})
    isThere = os.path.exists("session_data/typing_speeds.csv"); mode = 'a' if isThere else 'w'
    df.to_csv("session_data/typing_speeds.csv", mode=mode, index=False, header=not isThere)

    count = Counter(data['inputString'])
    global KEY_DIST
    KEY_DIST = KEY_DIST + count
    return '0'

@app.route('/get_image')
def get_image():
    if KEY_DIST:
        khm = KeyHeatMap()
        KEY_DIST.pop(' ', None)
        image_array = khm.plot(KEY_DIST)
        image_pil = Image.fromarray(image_array)
    else: image_pil = Image.open('assets/MK101.jpg')

    byte_stream = BytesIO()
    image_pil.save(byte_stream, format='JPEG')
    byte_stream.seek(0)
    return send_file(byte_stream, mimetype='image/jpeg', as_attachment=True, download_name='image.jpg')

if __name__ == '__main__':
    
    session_output_path = './session_data/raw'
    if not os.path.exists(session_output_path):
        os.makedirs(session_output_path, exist_ok=True)
    
    app.run(debug=False)