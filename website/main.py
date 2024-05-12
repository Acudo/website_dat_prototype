from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/process_data', methods=['POST'])
def process_data():
    input_data = request.form['input_data']
    with open("returned_inputs.txt", "a") as f:
        f.write(input_data + '\n')
    return 'Data processed: ' + input_data


@app.route('/update_streak', methods=['POST'])
def update_streak():
    print("hello")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
