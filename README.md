# myCrud

Site basico para controlar banco de dados

# COMANDO:
pip install mysql-connector-python

# SQL:
CREATE DATABASE meu_banco;

USE meu_banco;

CREATE TABLE alunos (
    id CHAR(36) DEFAULT (UUID()) PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    idade INT NOT NULL,
    turma VARCHAR(50) NOT NULL
);
