from flask import Flask, request, render_template, jsonify, url_for
import time
from url2text import url2text
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def predict():
    """ Main webpage with user input through form and prediction displayed

    :return: main webpage host, displays prediction if user submitted in text field
    """

    if request.method == 'POST':
        response = request.form['text']
        prediction = url2text(response)
        return render_template('index.html', text=prediction, submission=response)

    if request.method == 'GET':
        return render_template('index.html')


# TODO: add versioning to api
@app.route('/predict', methods=['POST'])
def predict_api():
    """ endpoint for model queries (non gui)

    :return: json, model prediction and response time
    """
    start_time = time.time()

    request_data = request.json
    input_text = request_data['data']
    prediction = url2text(input_text)
    response = {'prediction': prediction, 'response_time': time.time() - start_time}
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
