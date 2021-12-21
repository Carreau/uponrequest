from flask import Flask, request
import os
from textwrap import indent
from there import print


app = Flask(__name__)

import sendgrid
import os
from sendgrid.helpers.mail import Mail, Email, To, Content, Header, ReplyTo


def parse_header(heads):
    values = {}
    for l in heads.splitlines():
        k, v = l.split(":", maxsplit=1)
        values[k] = v
    return values


def reply(msg):
    print("vvvvvvvvvv")
    headers = parse_header(msg['headers'])
    print('Parsed Headers': headers)
    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get("SENDGRID_TOKEN"))
    from_email = Email("test@parse.availableuponrequest.org")
    to_email = To(msg["from"])  # Change to your recipient
    subject = "Re: " + msg["subject"]
    content = Content("text/plain", "Reply\n" + indent(msg["text"], "> "))
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

    if to_email.email != "bussonniermatthias@gmail.com":
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


@app.route('/email', methods=['POST'])
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
    ap.run(host="0.0.0.0", port=int(env.get("PORT", 5000)))
