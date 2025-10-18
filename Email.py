import smtplib
import pandas as pd
import datetime

def send_email(address, subject, message):
    my_email = "dradigitalmessenger@gmail.com"
    password = "mxwc ojhl jiwg bptq"
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(from_addr=my_email, to_addrs=address, msg=f"Subject:{subject}\n\n{message}")

month = datetime.datetime.now().month
day = datetime.datetime.now().day





