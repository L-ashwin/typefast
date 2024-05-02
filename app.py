import random
from flask import Flask, render_template

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
        data = data.split('***')
    return random.choice(data).strip().replace('‘', "'").replace('’', "'").replace('“', '"').replace('”', '"')

if __name__ == '__main__':
    app.run(debug=False)