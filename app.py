import random, datetime, json, os
from flask import Flask, render_template, request

app=Flask(__name__)

# Define a route to serve the index.html file
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_string', methods=['POST'])
def get_string():
    file_name = 'naval-tweets.md' # text file with tweets seperated by ***
    with open(file_name, 'r') as file:
        data =  file.read()
        data = data.split('***')[1:]
    return random.choice(data).strip().replace('‘', "'").replace('’', "'").replace('“', '"').replace('”', '"')

@app.route('/save_data', methods=['POST'])
def save_data():
    data = request.get_json()

    current_datetime = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = f'session_data/typefase_{current_datetime}.json'

    with open(filename, 'w') as file:
        json.dump(data, file)
    
    return '0'


if __name__ == '__main__':
    
    if not os.path.exists('./session_data'):
        os.mkdir('./session_data')
    
    app.run(debug=False)