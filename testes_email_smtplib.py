# -*- coding: utf-8 -*-
"""
Created on Sat Feb 13 16:19:24 2021

@author: GREYJOY
"""
import smtplib

sender_email = "clecio.antao@gmail.com"
rec_email = "clecio.antao@gmail.com"
password = "Proteu690201@"
subject = "Testando"
message = "Hey, this was sent using python"

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(sender_email, password)
print("Login success")
server.sendmail(sender_email, rec_email, message)


print("Email has been sent to ", rec_email)




"""
import csv

with open("contacts_file.csv") as file:
    reader = csv.reader(file)
    next(reader)  # Skip header row
    for name, email, grade in reader:
        print(f"Sending email to {name}")
        # Send email here
"""