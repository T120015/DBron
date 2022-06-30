CREATE DATABASE if NOT EXISTS dbron06;

DROP TABLE if EXISTS uriage;
DROP TABLE if EXISTS customer;

CREATE TABLE customer(
    customerID int NOT NULL AUTO_INCREMENT,
    namae varchar(30),
    c_address VARCHAR(50),
    tell VARCHAR(20),
    tantou VARCHAR(30),
    delflag BOOL DEFAULT FALSE
    PRIMARY KEY(customerID)
);

CREATE TABLE uriage(
    uriageID INT NOT NULL AUTO_INCREMENT,
    customerID INT,
    uriagegaku INT,
    uriagedate DATE,
    PRIMARY KEY(uriageID),
    FOREIGN KEY(customerID)
        REFERENCES customer(customerID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);