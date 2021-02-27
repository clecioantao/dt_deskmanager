# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 13:31:57 2021
@author: Clecio Antao
Rotina para leitura de API Desk Manager para popular tabela SQL Server
"""
def carrega_dados_relatorio():
    
    import pandas as pd
    import requests
    import json
    import sqlalchemy
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    from datetime import datetime
            
    # CRIA ENGINE DE ORIGEM - CONNECT SQL SERVER
    
    engineorigem = sqlalchemy.create_engine('mssql+pyodbc://sa:Proteu690201@192.168.2.150/deskmanager?driver=SQL Server')
        
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
    
    # VERIFICA QUANTIDADE DE REGISTROS
    url = "https://api.desk.ms/Relatorios/imprimir"
    paginador = '\"' +  ' ' + '\"'
    relatorio = "837"
    payload="{\r\n  \"Chave\":\"837\", \r\n  \"APartirDe\":\"\", \r\n  \"Total\":\"\"\r\n}"
    #payload="{\r\n  \"Chave\" :"  + relatorio +  ", \r\n  \"APartirDe\" : \" " + paginador + ", \r\n  \"Total\": \"\" \r\n}"
    headers = {
      'Authorization': resp_token,
      'Content-Type': 'application/json'
    }
    resp = requests.request("POST", url, headers=headers, data=payload)
    resp_data = json.loads(resp.text)
    root = resp_data['root']
    df = pd.DataFrame(root)
    index = df.index
    total_linhas = len(index)
    print('Total de linhas: ', total_linhas)
    
    # CRIAR LAÇO 
    print(resp_token)
    
    #chamados_total =  100000
    chamados_pag = 0
    paginas = 100000 #round((chamados_total / 5000) + 0.5)
    contador = 1
      
    while contador <= paginas:
        print('entrou no laço')
        print('Paginas: ', paginas)
        print('Contador: ', contador)
        print('Linhas: ',chamados_pag)
        print('Colunas: ',len(df.columns))
        #################################
        # LISTA DE CHAMADOS - paginação de 3000 em 3000 
        url = "https://api.desk.ms/Relatorios/imprimir"
        paginador = '\"' +  str(chamados_pag) + '\"'
        relatorio = "837"
        payload="{\r\n  \"Chave\" :"  + relatorio +  ", \r\n  \"APartirDe\" :" + paginador + ", \r\n  \"Total\": \"\" \r\n}"
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
        if len(df.columns) == 30:
            cs = 2097 // len(df.columns)  # duas barras faz a divisão e tras numero inteiro
            if cs > 1000:
                cs = 1000
            else:
                cs = cs
        else:
            break
        # INSERE DADOS TABELA SQL SEVER
        if chamados_pag == 0:
            df.to_sql(name='relatorios', con=engineorigem, if_exists='replace', chunksize=cs)
        else:
            df.to_sql(name='relatorios', con=engineorigem, if_exists='append', chunksize=cs)
            
        chamados_pag = chamados_pag + 5000
        contador =  contador + 1

    ### SEGUNDA PARTE
    
    #from popula_sql_api_deskmanager import carrega_dados
    
    # FAZ CONEXÃO COM BANCO
    
    # Todos chamados *
    chamados = pd.read_sql(sql="SELECT * FROM chamados", con=engineorigem)
    # Chamados aguardando atendimento na fila
    chamados_aa_fila = pd.read_sql(sql="select * from relatorios where NomeStatus = 'AGUARDANDO ATENDIMENTO' and NomeOperador is null order by 3 ", con=engineorigem)
    # chamados aguardando atendimento com analista
    chamados_aa_analista = pd.read_sql(sql="select * from relatorios where NomeStatus = 'AGUARDANDO ATENDIMENTO' and NomeOperador is not null order by 4,5 ", con=engineorigem)
    # chamados aguardando ações expirado nivel 1
    chamados_aguardando_expn1 = pd.read_sql(sql="select * from relatorios where (NomeStatus = 'AGUARDANDO ATENDIMENTO' OR  NomeStatus = 'ANDAMENTO') and (Sla1Expirado = 'Expirado' and Sla2Expirado = 'Em Dia') order by 4,5 ", con=engineorigem)
    # chamados aguardando ações em dia
    chamados_aguardando_emdia = pd.read_sql(sql="select * from relatorios where (NomeStatus = 'AGUARDANDO ATENDIMENTO' OR  NomeStatus = 'ANDAMENTO') and (Sla1Expirado = 'Em Dia' and Sla2Expirado = 'Em Dia') order by 4,5 ", con=engineorigem)
    # chamados aguardando ações expirados
    chamados_aguardando_expirados = pd.read_sql(sql="select * from relatorios where (NomeStatus = 'AGUARDANDO ATENDIMENTO' OR  NomeStatus = 'ANDAMENTO') and (Sla1Expirado = 'Expirado' and Sla2Expirado = 'Expirado') order by 4,5 ", con=engineorigem)
    
    chamados.set_index('Chave', inplace=True)
    
    # Quantidade de chamados abertos
    print(len(chamados['CodChamado'].index))
    print(chamados.iloc[:, [1,2]][chamados.NomeStatus =='AGUARDANDO ATENDIMENTO'])
    print(chamados_aa_analista[['NomeOperador', 'CodChamado']])
    
    #### DISPARA E-MAIL
    
    sumario_html = """
    <html>
    <head>
    <style>
    p.center {
      text-align: left;
      border: 1px solid black;
      border-collapse: collapse;
      padding: 10px;
      vertical-align: baseline;
    }
    p.titulo {
      font-size: 200%;
      color: red;
    }
    p.subtitulo {
      font-size: 150%;
      color: black;
    }
    p.anuncio {
      font-size: 120%;
      color: black;
      border: 0px;
    }
    
    table, th, td {
      margin: 2px;
      padding: 5px;
      border: 1px solid black;
      border-collapse: collapse;
      vertical-align: baseline;
      text-align: left;  
      background-color: #fff;
    }
    
    </style>
    </head>
    <body>
    
    </body>
    </html>
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
    
    titulo = '<p class="center titulo">ETL Desk Manager - TI-Sistemas</p>'
    
    now = datetime.now()
    qtd_chamados = '<p class="center subtitulo"> Registros Carregados: ' + str(len(chamados['CodChamado'].index)) + ' - Data: ' + str(now.day)+'/'+str(now.month)+'/'+str(now.year) + ' - ' + str(now.hour)+':'+str(now.minute)+':'+str(now.second) + '</p>'
    
    subtit1 = '<p class="center anuncio"><b>AGUARDANDO AÇÃO - EXPIRADOS 1º ATENDIMENTO</h3></b></p>'
    dados1 = chamados_aguardando_expn1[['CodChamado', 'Assunto', 'DataCriacao', 'NomeStatus', 'Sla1Expirado', 'Sla2Expirado', 'NomeOperador']].to_html(index=False) 
    
    subtit2 = '<p class="center anuncio"><b>AGUARDANDO AÇÃO - EM DIA</h3></b></p>'
    dados2 = chamados_aguardando_emdia[['CodChamado', 'Assunto', 'DataCriacao', 'NomeStatus', 'Sla1Expirado', 'Sla2Expirado', 'NomeOperador']].to_html(index=False) 
    
    subtit3 = '<p class="center anuncio"><b>AGUARDANDO AÇÃO - EXPIRADOS</h3></b></p>'
    dados3 = chamados_aguardando_expirados[['CodChamado', 'Assunto', 'DataCriacao', 'NomeStatus', 'Sla1Expirado', 'Sla2Expirado', 'NomeOperador']].to_html(index=False) 
    
    # Record the MIME types of both parts - text/plain and text/html.
    sumario = MIMEText(sumario_html, 'html')
    titulo = MIMEText(titulo, 'html')
    registros = MIMEText(qtd_chamados, 'html')
    part1 = MIMEText(subtit1, 'html')
    part2 = MIMEText(dados1, 'html')
    part3 = MIMEText(subtit2, 'html')
    part4 = MIMEText(dados2, 'html')
    part5 = MIMEText(subtit3, 'html')
    part6 = MIMEText(dados3, 'html')
    
    message.attach(sumario)
    message.attach(titulo)
    message.attach(registros)
    message.attach(part1)
    message.attach(part2)
    message.attach(part3)
    message.attach(part4)
    message.attach(part5)
    message.attach(part6)
    
    # conectaremos de forma segura usando SSL
    server = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
    # para interagir com um servidor externo precisaremos
    # fazer login nele
    server.login(username, password)
    server.sendmail(from_addr, to_addrs, message.as_string())
    server.quit()