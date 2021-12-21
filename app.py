from flask import Flask, request

app = Flask(__name__)


@app.route("/")
def root():
    print("working")
    return "slash"


@app.route("/test")
def test():
    print("working")
    return "ok"


@app.route('/email', methods=['POST'])
def receive_email():
    print('From:', request.form['from'])
    print('To:', request.form['to'])
    print('Subject:', request.form['subject'])
    print('Body:', request.form['text'])
    return ''
