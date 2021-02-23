# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 17:17:19 2021

@author: GREYJOY
"""
import pandas as pd
import requests
import json
import sqlalchemy

# CRIA ENGINE DE ORIGEM - CONECT SQL SERVER

engineorigem = sqlalchemy.create_engine('mssql+pyodbc://sa:Proteu690201@192.168.2.20/curso?driver=SQL Server')

# AUTENTICAÇÃO API
url = "https://api.desk.ms/Login/autenticar"
pubkey = '\"ef89a6460dbd71f2e37a999514d2543b99509d4f\"'
payload=" {\r\n  \"PublicKey\" :" + pubkey + "\r\n}"
headers = {
  'Authorization': '66e22b87364fa2946f2ce04dce1b8b59b669ab7f',
  'Content-Type': 'application/json'
}
token = requests.request("POST", url, headers=headers, data=payload)
resp_token = json.loads(token.text)

# CRIAR LAÇO 


chamados_pag = 3000


#################################
# LISTA DE CHAMADOS - paginação de 3000 em 3000 
url = "https://api.desk.ms/ChamadosSuporte/lista"
pesquisa = '\"T.I. - Sistemas\"'
paginador = '\"' +  str(chamados_pag) + '\"'
payload="{\r\n  \"Pesquisa\" :"  + pesquisa +  ", \r\n  \"Tatual\" :" + paginador + ", \r\n  \"StatusSLA\": \"\" \r\n}"
headers = {
  'Authorization': resp_token,
  'Content-Type': 'application/json'
}
resp = requests.request("POST", url, headers=headers, data=payload)
resp_data = json.loads(resp.text)
root = resp_data['root']
df = pd.DataFrame(root)



# EXPORTANDO DADASET PARA TABELA BANCO SQL SERVER
# CALCULA O CHUNKSIZE MÁXIMO E VERIFICA FINAL LINHAS

# INSERE DADOS TABELA SQL SEVER

df.to_sql(name='chamados', con=engineorigem, if_exists='replace')

    

