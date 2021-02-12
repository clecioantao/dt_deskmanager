import pandas as pd
import requests
import json

#AUTENTICAÇÃO
"""
url = "https://api.desk.ms/Login/autenticar"

payload="{\r\n  \"PublicKey\": \"ef89a6460dbd71f2e37a999514d2543b99509d4f\"\r\n}"
headers = {
  'Authorization': '66e22b87364fa2946f2ce04dce1b8b59b669ab7f',
  'Content-Type': 'application/json'
}

token = requests.request("POST", url, headers=headers, data=payload)
"""


url = "https://api.desk.ms/ChamadosSuporte/lista"

payload="{\r\n  \"Pesquisa\":\"0221-006993\", \r\n  \"Tatual\":\"\", \r\n  \"StatusSLA\":\"\"\r\n}"
headers = {
  'Authorization': 'dGVjYmFu#6a5ccf8c08d95fba8295075d59fce26a87e0641b',
  'Content-Type': 'text/plain'
}

resp = requests.request("POST", url, headers=headers, data=payload)

resp_data = json.loads(resp.text)

root = resp_data['root']

df = pd.DataFrame(root)


#print(root)
print(df.dtypes)



#print(resp.json())