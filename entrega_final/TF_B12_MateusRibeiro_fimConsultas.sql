-- -------- < Trabalho Final - Dataming > --------
--
--                    SCRIPT DE CONSULTAS (DML)
--
-- Data Criacao ...........: 30/06/2024
-- Autor(es) ..............: João Lucas Pinto Vasconcelos
--                           Mateus Orlando Medeiros Ribeiro
--                           Zenilda Pedrosa Vieira
-- Banco de Dados .........: MySQL 8.0
-- Base de Dados (nome) ...: TFBD
--
-- PROJETO => 01 Base de Dados
--         => 04 Tabelas
--         => 02 Views
--         => 02 Consultas
--
-- Ultimas Alteracoes
--     
-- ----------------------------------------------------------------------------------------

-- A VIEW vw_gastos_mensais_deputados agrega os gastos mensais de cada deputado, 
-- apresentando o total de gastos por mês, a média dos gastos mensais, juntamente 
-- com o partido ao qual ele pertence, destacando os deputados 
-- que mais gasteram por mês (ordem decrescente de gastos totais)

CREATE VIEW vw_gastos_mensais_deputados AS
SELECT 
    d.id AS id_deputado,
    d.nome AS nome_deputado,
    p.sigla AS sigla_partido,
    p.nome AS nome_partido,
    YEAR(g.data) AS ano,
    MONTH(g.data) AS mes,
    SUM(g.valor) AS total_gastos_mensal,
    AVG(SUM(g.valor)) OVER(PARTITION BY d.id) AS media_gastos_mensais
FROM 
    deputados d
JOIN 
    gastos g ON d.id = g.id_deputado
JOIN 
    partidos p ON d.partido = p.sigla
GROUP BY 
    d.id, d.nome, p.sigla, p.nome, YEAR(g.data), MONTH(g.data)
ORDER BY 
    total_gastos_mensal DESC;


SELECT * FROM vw_gastos_mensais_deputados;

-- A VIEW  agrega os gastos totais por partido e por tipo de despesa de toda a 
-- câmara dos deputados. Fornece uma análise detalhada dos gastos totais de 
-- cada partido, categorizados por tipo de despesa.

CREATE VIEW vw_total_partido_tipo_gastos AS
SELECT 
    g.partido AS sigla_partido,
    p.nome AS nome_partido,
    g.tipoDespesa,
    SUM(g.valor) AS total_gastos
FROM 
    gastos g
JOIN 
    partidos p ON g.partido = p.sigla
GROUP BY 
    g.partido, p.nome, g.tipoDespesa
ORDER BY 
    g.partido, g.tipoDespesa;

SELECT * FROM vw_total_partido_tipo_gastos;
