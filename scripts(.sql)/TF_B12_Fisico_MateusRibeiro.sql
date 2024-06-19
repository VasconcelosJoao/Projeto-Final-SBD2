-- -------- < Trabalho Final - Dataming > --------
--
--                    SCRIPT DE CRIACAO (DDL)
--
-- Data Criacao ...........: 17/06/2024
-- Autor(es) ..............: João Lucas Pinto Vasconcelos
--                           Mateus Orlando Medeiros Ribeiro
--                           Zenilda Pedrosa Vieira
-- Banco de Dados .........: MySQL 8.0
-- Base de Dados (nome) ...: TFBD
--
-- PROJETO => 01 Base de Dados
--         => 08 Tabelas
--
-- 
-- Ultimas Alteracoes
--   
--   
-- ----------------------------------------------------------------------------------------

CREATE DATABASE IF NOT EXISTS TFBD;


USE TFBD;


CREATE TABLE IF NOT EXISTS partidos (
    sigla VARCHAR(50) PRIMARY KEY,
    nome VARCHAR(255)

) ENGINE = InnoDB;


CREATE TABLE IF NOT EXISTS deputados (
    id INT PRIMARY KEY,
    nome VARCHAR(255),
    partido VARCHAR(50),
    FOREIGN KEY (partido) REFERENCES partidos(sigla)
) ENGINE = InnoDB;


CREATE TABLE IF NOT EXISTS gastos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_deputado INT,
    data DATE,
    valor FLOAT,
    tipoDespesa VARCHAR(255),
    codDocumento INT,
    partido VARCHAR(50),
    FOREIGN KEY (id_deputado) REFERENCES deputados(id),
    FOREIGN KEY (partido) REFERENCES partidos(sigla)
) ENGINE = InnoDB AUTO_INCREMENT = 1;


CREATE TABLE IF NOT EXISTS gastos_estranhos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_deputado INT,
    data DATE,
    valor FLOAT,
    tipoDespesa VARCHAR(255),
    codDocumento INT,
    partido VARCHAR(50),
    FOREIGN KEY (id_deputado) REFERENCES deputados(id),
    FOREIGN KEY (partido) REFERENCES partidos(sigla)
) ENGINE = InnoDB AUTO_INCREMENT = 1;


CREATE TABLE IF NOT EXISTS resultados_regressao (
    id INT AUTO_INCREMENT PRIMARY KEY,
    coeficientes TEXT,
    erro_quadratico_medio FLOAT
) ENGINE = InnoDB AUTO_INCREMENT = 1;


CREATE TABLE IF NOT EXISTS top_spending_deputies (
    id_deputado INT PRIMARY KEY,
    valor FLOAT,
    nome VARCHAR(255)
) ENGINE=InnoDB;


CREATE TABLE IF NOT EXISTS top_spending_items (
    tipoDespesa VARCHAR(255) PRIMARY KEY,
    valor FLOAT
) ENGINE=InnoDB;


CREATE TABLE IF NOT EXISTS gasto_medio_mensal (
    id_deputado INT,
    ano INT,
    mes INT,
    valor FLOAT,
    PRIMARY KEY (id_deputado, ano, mes)
) ENGINE=InnoDB;

