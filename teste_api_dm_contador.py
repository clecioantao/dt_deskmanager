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

chamados_total = 71220
chamados_pag = 3000

paginas = round((chamados_total / chamados_pag) + 0.5)
print(paginas)
contador = 1

while contador <= paginas:

    #################################
    # LISTA DE CHAMADOS - paginação de 3000 em 3000
    
    url = "https://api.desk.ms/ChamadosSuporte/lista"
    payload="{\r\n  \"Pesquisa\":\"T.I. Sistemas\", \r\n  \"Tatual\":\"chamados_pag\", \r\n  \"StatusSLA\": \"\"\r\n}"
    #payload2="{\r\n  \"Pesquisa\":\"T.I. Sistemas\", \r\n  \"Tatual\":\"chamados_pag\", \r\n  \"StatusSLA\": \"\"\r\n}"


    headers = {
      'Authorization': resp_token,
      'Content-Type': 'application/json'
    }
    resp = requests.request("POST", url, headers=headers, data=payload)
    resp_data = json.loads(resp.text)
    root = resp_data['root']
    
    #df = df + str(contador)
    
    df = pd.DataFrame(root)
    
    print(payload)
    print(chamados_pag)
    print(contador)
   
    # EXPORTA TABELA PARA O BANCO
    
    # CALCULA O CHUNKSIZE MÁXIMO
    cs = 2097 // len(df.columns)  # duas barras faz a divisão e tras numero inteiro
    if cs > 1000:
        cs = 1000
    else:
        cs = cs
    # INSERE DADOS TABELA SQL SEVER
    df.to_sql(name='chamados', con=engineorigem, if_exists='append', chunksize=cs)
    
    chamados_pag = chamados_pag + 3000
    contador =  contador + 1
    
 