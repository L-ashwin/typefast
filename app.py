import pandas as pd
import random, datetime, json, os
from flask import Flask, render_template, request

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

    return '0'


if __name__ == '__main__':
    
    session_output_path = './session_data/raw'
    if not os.path.exists(session_output_path):
        os.makedirs(session_output_path, exist_ok=True)
    
    app.run(debug=False)