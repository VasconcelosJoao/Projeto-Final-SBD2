-- -------- < Trabalho Final - Dataming > --------
--
--                    SCRIPT DE CRIACAO (DDL)
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

CREATE DATABASE IF NOT EXISTS TFBD;


USE TFBD;


CREATE TABLE partidos (
    sigla VARCHAR(50) NOT NULL,
    nome VARCHAR(255),

    CONSTRAINT PARTIDOS_PK PRIMARY KEY (sigla)

) ENGINE = InnoDB;


CREATE TABLE deputados (
    id INT NOT NULL,
    nome VARCHAR(255),
    partido VARCHAR(50),

    CONSTRAINT DEPUTADOS_PK PRIMARY KEY (id),

    CONSTRAINT DEPUTADOS_PARTIDOS_FK FOREIGN KEY (partido) 
        REFERENCES partidos(sigla)
            ON DELETE RESTRICT
            ON UPDATE RESTRICT

) ENGINE = InnoDB;


CREATE TABLE gastos (
    id INT NOT NULL AUTO_INCREMENT,
    id_deputado INT,
    data DATE,
    valor FLOAT,
    tipoDespesa VARCHAR(255),
    codDocumento INT,

    CONSTRAINT GASTOS_PK PRIMARY KEY (id),
    
    CONSTRAINT GASTOS_DEPUTADOS_FK FOREIGN KEY (id_deputado) 
        REFERENCES deputados(id)
            ON DELETE RESTRICT
            ON UPDATE RESTRICT

) ENGINE = InnoDB AUTO_INCREMENT = 1;


CREATE TABLE gastos_estranhos (
    id INT NOT NULL AUTO_INCREMENT,
    id_deputado INT,
    data DATE,
    valor FLOAT,
    tipoDespesa VARCHAR(255),
    codDocumento INT,

    CONSTRAINT GASTOS_ESTRANHOS_PK PRIMARY KEY (id),
    
    CONSTRAINT GASTOS_ESTRANHOS_DEPUTADOS_FK FOREIGN KEY (id_deputado) 
        REFERENCES deputados(id)
            ON DELETE RESTRICT
            ON UPDATE RESTRICT

) ENGINE = InnoDB AUTO_INCREMENT = 1;

CREATE INDEX gastos_tipoDespesa_idx ON gastos(tipoDespesa);
CREATE INDEX gastos_estranhos_tipoDespesa_idx ON gastos_estranhos(tipoDespesa);
