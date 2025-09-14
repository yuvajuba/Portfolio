from flask import Flask, render_template, request, redirect
import datetime
import os
import textwrap
# import csv

import smtplib
from email.message import EmailMessage
from string import Template
from pathlib import Path

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/<string:page_name>")
def html_page(page_name):
    return render_template(page_name)


if not os.path.exists("./database.txt"):
    open("./database.txt", mode="w").close()

# if not os.path.exists("./database.csv"):
#     open("./database.csv", mode="w").close()
#     with open("./database.csv", "w") as f:
#         f.write("Date,Email,Subject,Message\n")


def store_data(data):
    with open("ident.txt", "r") as f:
        lines = f.read().splitlines()
        data["sender"] = lines[0].strip()
        data["password"] = lines[1].strip()

    fullname = data["fullname"]
    email = data["email"]
    subject = data["subject"]
    message = data["message"]
    time = datetime.date.today()
    
    with open("./database.txt", "a", encoding='utf-8') as file:      
        file.write(f'Submition date     : {time}\n')
        file.write(f'Full name          : {fullname}\n')
        file.write(f'Email              : {email}\n')
        file.write(f'Subject            : {subject}\n')
        file.write(f'Message \n')
        file.write(f'↓↓↓↓↓↓↓ \n')
        file.write(f'{textwrap.fill(message, width=80)}\n\n\n\n')
    
    # with open("./database.csv", mode="a", newline='', encoding='utf-8') as file2:
    #     csv_writer = csv.writer(file2, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
    #     csv_writer.writerow([time,email,subject,message])

    return data



# Set the thankyou page and sending the message notification !
##############################################################
@app.route('/contact', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        try:
            data = request.form.to_dict()
            data = store_data(data)

            html_tpl = Template(Path("templates/message.html").read_text())
            html_bdy = html_tpl.substitute({"name": data["fullname"]})

            email = EmailMessage()
            email["from"] = "Juba Bennour"
            email["to"] = data["email"]
            email["subject"] = "Auto reply message!"
            email.set_content(html_bdy, "html")

            with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
                smtp.ehlo()
                smtp.starttls()
                smtp.login(data["sender"], data["password"])
                smtp.send_message(email)

            return redirect("/thankyou.html")
        except Exception as e:
            return f"Error: {e}"
    else:
        return 'Something went wrong! check it out'


