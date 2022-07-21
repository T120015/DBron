CREATE DATABASE if NOT EXISTS dbron09;
USE dbron09;

DROP TABLE if EXISTS shosai;
DROP TABLE if EXISTS tyumon;
DROP TABLE if EXISTS client;
DROP TABLE if EXISTS product;

CREATE TABLE client(
    clientID INT NOT NULL AUTO_INCREMENT,
    namae VARCHAR(45) NOT NULL,
    areanum VARCHAR(10),
    prefecture VARCHAR(10),
    city VARCHAR(30),
    street VARCHAR(30),
    remarks VARCHAR(40),
    lastupdate DATETIME DEFAULT NOW(),
    delflag BOOL DEFAULT False,
    PRIMARY KEY(clientID)
);

CREATE TABLE product(
    productID INT NOT NULL AUTO_INCREMENT,
    productkey VARCHAR(10) NOT NULL UNIQUE,
    productname VARCHAR(30) NOT NULL,
    unitprice INT NOT NULL,
    lastupdate DATETIME DEFAULT NOW(),
    delflag BOOL DEFAULT False,
    PRIMARY KEY(productID)
);

CREATE TABLE tyumon(
    orderID INT NOT NULL AUTO_INCREMENT,
    clientID INT,
    pastage INT,
    lastupdate DATETIME DEFAULT NOW(),
    delflag BOOL DEFAULT False,
    PRIMARY KEY(orderID),
    FOREIGN KEY(clientID)
        REFERENCES client(clientID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE shosai(
    shosaiID INT NOT NULL AUTO_INCREMENT,
    applicationID INT,
    orderID INT,
    productkey VARCHAR(10),
    quantity INT,
    lastupdate DATETIME DEFAULT NOW(),
    delflag BOOL DEFAULT False,
    PRIMARY KEY(shosaiID),
    FOREIGN KEY(orderID)
        REFERENCES tyumon(orderID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY(productkey)
        REFERENCES product(productkey)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);