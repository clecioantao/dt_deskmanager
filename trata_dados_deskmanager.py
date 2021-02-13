# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 13:31:57 2021
@author: Clecio Antao

Rotina para tratar dados Desk Manager e apresentar qa

"""

import pandas as pd
import sqlalchemy
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# EXECUTA ROTINA PARA POPULAR TABELA SQL SERVER
#import popula_sql_api_deskmanager.py

#from popula_sql_api_deskmanager import carrega_dados
#carrega_dados()

# FAZ CONEXÃO COM BANCO
engineorigem = sqlalchemy.create_engine('mssql+pyodbc://sa:Proteu690201@192.168.2.20/curso?driver=SQL Server')

total_chamados = pd.read_sql(sql="SELECT count(*) FROM chamados", con=engineorigem)

# Todos chamados *
chamados = pd.read_sql(sql="SELECT * FROM chamados", con=engineorigem)
# Chamados aguardando atendimento na fila
chamados_aa_fila = pd.read_sql(sql="select * from chamados where NomeStatus = 'AGUARDANDO ATENDIMENTO' and NomeOperador is null order by 3 ", con=engineorigem)
# chamados aguardando atendimento com analista
chamados_aa_analista = pd.read_sql(sql="select * from chamados where NomeStatus = 'AGUARDANDO ATENDIMENTO' and NomeOperador is not null order by 4,5 ", con=engineorigem)

chamados.set_index('Chave', inplace=True)

# Quantidade de chamados abertos
print(len(chamados['CodChamado'].index))

print(chamados.iloc[:, [1,2]][chamados.NomeStatus =='AGUARDANDO ATENDIMENTO'])

#print(chamados_aa_analista[['NomeOperador', 'CodChamado']].to_html(classes='table table-striped'))
#print(chamados_aa_analista.to_html(classes='table table-striped'))
print(chamados_aa_analista[['NomeOperador', 'CodChamado']])

#### DISPARA E-MAIL

mystyle = """
.mystyle {
    font-size: 15pt; 
    font-family: Arial;
    border-collapse: collapse; 
    border: 1px solid silver;

}
.mystyle td, th {
    padding: 15px;
}
.mystyle tr:nth-child(even) {
    background: #E0E0E0;
}
.mystyle tr:hover {
    background: silver;
    cursor: pointer;
}
"""

# conexão com os servidores do google
smtp_ssl_host = 'smtp.gmail.com'
smtp_ssl_port = 465
# username ou email para logar no servidor
username = 'clecio.antao@gmail.com'
password = 'Proteu690201@'
from_addr = 'clecio.antao@gmail.com'
to_addrs = ['clecio.antao@gmail.com']

# a biblioteca email possuí vários templates
# para diferentes formatos de mensagem
# neste caso usaremos MIMEText para enviar
# somente texto
message = MIMEMultipart('ETL - TI SISTEMAS')
message['subject'] = 'ETL TI-Sistemas'
message['from'] = from_addr
message['to'] = ', '.join(to_addrs)

# Create the body of the message (a plain-text and an HTML version).

titulo = '<h1>ETL Desk Manager - TI-Sistemas</h1>'

now = datetime.now()
qtd_chamados = '<h2> Registros Carregados: ' + str(len(chamados['CodChamado'].index)) + ' - Data: ' + str(now.day)+'/'+str(now.month)+'/'+str(now.year) + ' - ' + str(now.hour)+':'+str(now.minute)+':'+str(now.second)

subtit1 = "<h3> Status: <b>AGUARDANDO ATENDIMENTO</b> - CHAMADOS COM ANALISTAS</h3>"
dados1 = chamados_aa_analista[['NomeOperador', 'CodChamado', 'DataCriacao', 'Assunto' ]].to_html(index=False, border=1, classes=mystyle) 

subtit2 = "<h3> Status: <b>AGUARDANDO ATENDIMENTO</b> - CHAMADOS EM FILA</h3>"
dados2 = chamados_aa_fila[['NomeOperador', 'CodChamado', 'DataCriacao', 'Assunto' ]].to_html(index=False, border=1, classes=mystyle) 

# Record the MIME types of both parts - text/plain and text/html.
titulo = MIMEText(titulo, 'html')
registros = MIMEText(qtd_chamados, 'html')
part1 = MIMEText(subtit1, 'html')
part2 = MIMEText(dados1, 'html')
part3 = MIMEText(subtit2, 'html')
part4 = MIMEText(dados2, 'html')


message.attach(titulo)
message.attach(registros)
message.attach(part1)
message.attach(part2)
message.attach(part3)
message.attach(part4)

# conectaremos de forma segura usando SSL
server = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
# para interagir com um servidor externo precisaremos
# fazer login nele
server.login(username, password)
server.sendmail(from_addr, to_addrs, message.as_string())
server.quit()