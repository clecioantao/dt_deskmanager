# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 08:03:30 2021

@author: Clecio
"""

import pandas as pd
import requests
import json

#AUTENTICAÇÃO

url = "https://api.desk.ms/Login/autenticar"

payload = {
  'PublicKey': 'ef89a6460dbd71f2e37a999514d2543b99509d4f'
}
#payload="{\r\n  \"PublicKey\": \"ef89a6460dbd71f2e37a999514d2543b99509d4f\"\r\n}"
headers = {
  'Authorization': '66e22b87364fa2946f2ce04dce1b8b59b669ab7f',
  'Content-Type': 'text/plain'
}
token = requests.request("POST", url, headers=headers, data=payload)
resp_token = json.loads(token.text)

################

url = "https://api.desk.ms/ChamadosSuporte/lista"

"""
payload = {
  'Pesquisa': '',
  'Tatual': '', 
  'StatusSLA': ''
}
"""
payload="{\r\n  \"Pesquisa\":\"\", \r\n  \"Tatual\":\"\", \r\n  \"StatusSLA\":\"\"\r\n}"

headers = {
  'Authorization': resp_token,
  'Content-Type': 'application/json'
}

resp = requests.request("POST", url, headers=headers, data=payload)
resp_data = json.loads(resp.text)

root = resp_data['root']

df = pd.DataFrame(root)

print(df.iloc[:,:6])


