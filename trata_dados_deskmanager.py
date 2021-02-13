# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 13:31:57 2021
@author: Clecio Antao

Rotina para tratar dados Desk Manager e apresentar qa

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

chamados_total = 100000
chamados_pag = 3000
paginas = round((chamados_total / chamados_pag) + 0.5)
print(paginas)
contador = 1

while contador <= paginas:
    #################################
    # LISTA DE CHAMADOS - paginação de 3000 em 3000 
    url = "https://api.desk.ms/ChamadosSuporte/lista"
    pesquisa = '\"T.I. Sistemas\"'
    paginador = '\"' +  str(chamados_pag) + '\"'
    payload="{\r\n  \"Pesquisa\" :"  + pesquisa +  ", \r\n  \"Tatual\" :" + paginador + ", \r\n  \"StatusSLA\": \"\" \r\n}"
    headers = {
      'Authorization': resp_token,
      'Content-Type': 'application/json'
    }
    resp = requests.request("POST", url, headers=headers, data=payload)
    resp_data = json.loads(resp.text)
    print(type(resp_data))
    root = resp_data['root']
    df = pd.DataFrame(root)
    print(payload)
    print(chamados_pag)
    print(contador)
   
    # EXPORTANDO DADASET PARA TABELA BANCO SQL SERVER
    # CALCULA O CHUNKSIZE MÁXIMO E VERIFICA FINAL LINHAS
    if len(df.columns) > 0:
        cs = 2097 // len(df.columns)  # duas barras faz a divisão e tras numero inteiro
        if cs > 1000:
            cs = 1000
        else:
            cs = cs
    else:
        break
    # INSERE DADOS TABELA SQL SEVER
    if chamados_pag == 3000:
        df.to_sql(name='chamados', con=engineorigem, if_exists='replace', chunksize=cs)
    else:
        df.to_sql(name='chamados', con=engineorigem, if_exists='append', chunksize=cs)
        
    chamados_pag = chamados_pag + 3000
    contador =  contador + 1
print(chamados_pag)