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
--         => 04 Tabelas
--         => 02 Views
--         => 02 Consultas
--
-- Ultimas Alteracoes
--   
-- 01/07/2024 => atualização do Físico   
--
-- ----------------------------------------------------------------------------------------

CREATE DATABASE IF NOT EXISTS TFBD;


USE TFBD;


CREATE TABLE partidos (
    sigla VARCHAR(50) PRIMARY KEY,
    nome VARCHAR(255)

) ENGINE = InnoDB;


CREATE TABLE deputados (
    id INT PRIMARY KEY,
    nome VARCHAR(255),
    partido VARCHAR(50),
    FOREIGN KEY (partido) REFERENCES partidos(sigla)
) ENGINE = InnoDB;


CREATE TABLE gastos (
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


CREATE TABLE gastos_estranhos (
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


