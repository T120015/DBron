-- fuku0501.sql 
CREATE DATABASE if not exists dbron05;
USE dbron05;
DROP TABLE if exists meibo;
-- 【テーブル定義のSQL】
CREATE TABLE meibo(
    meiboID INT NOT NULL AUTO_INCREMENT,
    gakuseki VARCHAR(10) NOT NULL,
    namae VARCHAR(30) NOT NULL,
    yomi VARCHAR(50),
    acyear INT,
    math INT,
    eng INT,
    PRIMARY KEY(meiboID)
);
DESC meibo;
