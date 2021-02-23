# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 13:31:57 2021
@author: Clecio Antao

Rotina para leitura de API Desk Manager para popular tabela SQL Server

"""

import pandas as pd
import requests
import json
import sqlalchemy

# CRIA ENGINE DE ORIGEM - CONECT SQL SERVER

engineorigem = sqlalchemy.create_engine('mssql+pyodbc://sa:Proteu690201@192.168.2.20/curso?driver=SQL Server')

# AUTENTICAÇÃO API

url = "https://api.desk.ms/Login/autenticar"
payload="{\r\n  \"PublicKey\": \"ef89a6460dbd71f2e37a999514d2543b99509d4f\"\r\n}"
headers = {
  'Authorization': '66e22b87364fa2946f2ce04dce1b8b59b669ab7f',
  'Content-Type': 'application/json'
}
token = requests.request("POST", url, headers=headers, data=payload)
resp_token = json.loads(token.text)


# CRIAR LAÇO 


#################################
# LISTA DE CHAMADOS - até 3000

url = "https://api.desk.ms/ChamadosSuporte"
payload="{\r\n  \"Chave\": \"444641\" \r\n}"
pay = {
  'Chave': ''       
}
headers = {
  'Authorization': resp_token,
  'Content-Type': 'application/json'
}
resp = requests.request("POST", url, headers=headers, data=payload)
resp_data = json.loads(resp.text)

print(resp_data)


dados = resp_data['TChamado']
df1 = pd.DataFrame(dados)

print(df1)


#print(df1.iloc[:,:6])

# EXPORTA TABELA PARA O BANCO

# CALCULA O CHUNKSIZE MÁXIMO
cs = 2097 // len(df1.columns)  # duas barras faz a divisão e tras numero inteiro
if cs > 1000:
    cs = 1000
else:
    cs = cs
# INSERE DADOS TABELA SQL SEVER
df1['CodChamado'].to_sql(name='ChamadosSuporte', con=engineorigem, if_exists='replace', chunksize=cs)

