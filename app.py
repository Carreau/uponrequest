from flask import Flask, request
import os

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
    print("Headers:", request.form["headers"])
    print("From:", request.form["from"])
    print("To:", request.form["to"])
    print("Subject:", request.form["subject"])
    print("Body:", request.form["text"])
    return ""


if __name__ == "__main__":
    print("MAIN")
    ap.run(host="0.0.0.0", port=int(env.get("PORT", 5000)))
