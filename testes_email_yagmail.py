# -*- coding: utf-8 -*-
"""
Created on Sat Feb 13 16:52:46 2021

@author: GREYJOY
"""
import yagmail

receiver = "clecio.antao@gmail.com"
body = "Hello there from Yagmail"
filename = "document.pdf"

yag = yagmail.SMTP("clecio.antao@gmail.com")
yag.send(
    to=receiver,
    subject="Yagmail test with attachment",
    contents=body, 
    attachments=filename,
)