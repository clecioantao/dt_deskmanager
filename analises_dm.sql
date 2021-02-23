use deskmanager

select CodChamado, * from chamados
order by 6


select count(*) from chamados -- total chamados T.I Sistema 57046 -- Completo 200.125

SELECT COUNT(DISTINCT(CodChamado)) as [nao duplicados] FROM CHAMADOS

SELECT DISTINCT(NomeStatus) as [status] FROM CHAMADOS

select * from chamados -- total chamados T.I Sistema 57046 -- Completo 200.163

select count(*) from chamados
where NomeOperador like '%Leonardo%'
-- Assunto like '%DBA%'

select * from chamados where NomeStatus = 'AGUARDANDO ATENDIMENTO' and NomeOperador is not null order by 6,5

select 
NomeOperador, Sla1Expirado, Sla2Expirado, 
NomeStatus, CONVERT(VARCHAR(10),(CONVERT(DATETIME,DataCriacao,101)), 105) as DataCriacao, 
HoraCriacao, CONVERT(VARCHAR(10),(CONVERT(DATETIME,ExpiraEm,101)), 105) as Expiraem, DataAlteracao, HoraAlteracao,  * 
from chamados where NomeStatus = 'ANDAMENTO'



select  Sla1Expirado, Sla2Expirado, * from chamados where NomeStatus = 'AGUARDANDO ATENDIMENTO' and Sla1Expirado = 'N' and Sla2Expirado = 'N'

select  Sla1Expirado, Sla2Expirado, * from chamados where NomeStatus = 'AGUARDANDO ATENDIMENTO' and Sla2Expirado = 'N'

select  Sla1Expirado, Sla2Expirado, * from chamados where NomeStatus = 'AGUARDANDO ATENDIMENTO' and Sla1Expirado = 'S' and Sla2Expirado = 'N'

-- AGUARDANDO AÇÃO - EXPIRADO NOS DOIS NIVEIS
select NomeOperador, Sla1Expirado, Sla2Expirado, NomeStatus, DataCriacao, HoraCriacao, expiraem, DataAlteracao, HoraAlteracao,  * from chamados where (NomeStatus = 'AGUARDANDO ATENDIMENTO' OR  NomeStatus = 'ANDAMENTO') and (Sla1Expirado = 'S' and Sla2Expirado = 'S')
 
-- AGUARDANDO AÇÃO - EXPIRADO NO PRIMEIRO NIVEL
select NomeOperador, Sla1Expirado, Sla2Expirado, NomeStatus, DataCriacao, HoraCriacao, expiraem, DataAlteracao, HoraAlteracao,   * from chamados where (NomeStatus = 'AGUARDANDO ATENDIMENTO' OR  NomeStatus = 'ANDAMENTO') and (Sla1Expirado = 'S' and Sla2Expirado = 'N')

-- AGUARDANDO AÇÃO - NÃO EXPIRADOS
select NomeOperador, Sla1Expirado, Sla2Expirado, NomeStatus, DataCriacao, HoraCriacao, expiraem, DataAlteracao, HoraAlteracao,   * from chamados where (NomeStatus = 'AGUARDANDO ATENDIMENTO' OR  NomeStatus = 'ANDAMENTO') and (Sla1Expirado = 'N' and Sla2Expirado = 'N')

SELECT DataCriacao, NomeGrupo, Assunto, NomeStatus, * FROM CHAMADOS 
where NomeGrupo = 'T.I. - Sistemas'
order by 1 asc

SELECT NomeGrupo , DataCriacao, CodChamado, * FROM chamados 
where grupo
order by 2 desc

SELECT * FROM ChamadosSuporte