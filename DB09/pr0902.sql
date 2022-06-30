CREATE DATABASE IF NOT EXISTS dbron09;
USE dbron09;

DROP TABLE IF EXISTS shusseki;
DROP TABLE IF EXISTS jokyo;
DROP TABLE IF EXISTS class;
DROP TABLE IF EXISTS gakuseki;

CREATE TABLE gakuseki(
    gakusekiID int NOT NULL AUTO_INCREMENT,
    gakusekicode VARCHAR(10) NOT NULL UNIQUE,
    namae VARCHAR(30) NOT NULL,
    Ggteacher VARCHAR(30),
    Labo VARCHAR(30),
    lastupdate DATETIME DEFAULT NOW(),
    delflag BOOL DEFAULT False,
    PRIMARY KEY(gakusekiID)
);

CREATE TABLE class(
    classID int NOT NULL AUTO_INCREMENT,
    classcode VARCHAR(10) NOT NULL UNIQUE,
    classname VARCHAR(20) NOT NULL,
    week_period VARCHAR(10),
    teacher VARCHAR(30),
    lastupdate DATETIME DEFAULT NOW(),
    delflag BOOL DEFAULT False,
    PRIMARY KEY(classID)
);

CREATE TABLE jokyo(
    statusID int NOT NULL AUTO_INCREMENT,
    attendance VARCHAR(10)NOT NULL,
    lastupdate DATETIME DEFAULT NOW(),
    delflag BOOL DEFAULT False,
    PRIMARY KEY(statusID)
);

CREATE TABLE shusseki(
    shussekiID int not null auto_increment,
    gakusekicode varchar(10),
    classcode varchar(10),
    classcount int,
    classdays date,	
    statusID int,
    lastupdate datetime Default NOW(),
    delflag	bool Default False,
    PRIMARY KEY(shussekiID),
    FOREIGN KEY(gakusekicode)
        REFERENCES gakuseki(gakusekicode)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY(classcode)
        REFERENCES class(classID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY(statusID)
        REFERENCES jokyo(statusID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);