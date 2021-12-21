from flask import Flask, request
import os
from textwrap import indent


app = Flask(__name__)

import sendgrid
import os
from sendgrid.helpers.mail import Mail, Email, To, Content, Header, ReplyTo


def reply(msg):
    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get("SENDGRID_TOKEN"))
    from_email = Email("noreply@availableuponrequest.org")
    to_email = To(msg["from"])  # Change to your recipient
    subject = "Re: " + msg["subject"]
    content = Content("text/plain", "Reply\n" + indent(msg["text"], "> "))
    mail = Mail(from_email, to_email, subject, content)
    prev_id = msg.get("Message-ID", None)
    if prev_id:
        print("Found prev id:", prev_id)
        p = mail.personalizations[0]
        p.add_header(Header("In-Reply-To", prev_id))
        p.add_header(Header("References", prev_id))

    mail_json = mail.get()

    if to_email.email != "bussonniermatthias@gmail.com":
        print("Not to self", to_email.email)
        return
    # Send an HTTP POST request to /mail/send
    response = sg.client.mail.send.post(request_body=mail_json)
    print(response.status_code)
    print(response.headers)


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
    reply(request.form)
    return ""


if __name__ == "__main__":
    print("MAIN")
    ap.run(host="0.0.0.0", port=int(env.get("PORT", 5000)))
