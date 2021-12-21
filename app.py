from flask import Flask, request
import os
from textwrap import indent
from there import print
from random import choice


import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content, Header

app = Flask(__name__)


def parse_header(heads):
    values = {}
    for line in heads.splitlines():
        k, v = line.split(":", maxsplit=1)
        values[k] = v
    return values


REASONS = [
    "Thanks for your email, unfortunately the post doc that did the experiment is no longer in our lab.",
    "I appreciate your interest, I believe the data is on my old laptop. I'll try to find it 'soon' and get back to you",
    "Hello, I'm no longer in academia, please contact another author",
]


INCLUDE_USERS = ()


def reply(msg):
    print("vvvvvvvvvv")
    headers = parse_header(msg["headers"])
    print("Parsed Headers:", headers)
    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get("SENDGRID_TOKEN"))
    from_email = Email("noreply@availableuponrequest.org")
    to_email = To(msg["from"])  # Change to your recipient
    subject = "Re: " + msg["subject"]
    content = Content("text/plain", choice(REASONS) + "\n" + indent(msg["text"], "> "))
    mail = Mail(from_email, to_email, subject, content)
    prev_id = headers.get("Message-ID", None)
    print("Found prev id:", prev_id)
    print("-----")
    if prev_id:
        p = mail.personalizations[0]
        p.add_header(Header("In-Reply-To", prev_id))
        p.add_header(Header("References", prev_id))
    else:
        return

    mail_json = mail.get()

    if to_email.email not in INCLUDE_USERS:
        print("Not to self", to_email.email)
        return
    # Send an HTTP POST request to /mail/send
    response = sg.client.mail.send.post(request_body=mail_json)
    print("-----")
    print(response.status_code)
    print("-----")
    print(response.headers)
    print("^^^^^^^^")


@app.route("/")
def root():
    print("working")
    return "slash"


@app.route("/test")
def test():
    print("working")
    return "ok"


@app.route("/email", methods=["POST"])
def receive_email():
    print("Headers:", request.form["headers"])
    print("-----")
    print("From:", request.form["from"])
    print("-----")
    print("To:", request.form["to"])
    print("-----")
    print("Subject:", request.form["subject"])
    print("-----")
    print("Body:", request.form["text"])
    print("-----")
    reply(request.form)
    print("-----")
    return ""


if __name__ == "__main__":
    print("MAIN")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
