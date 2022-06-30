-- 演習2 pr0602-1.sql
USE dbron06;

DROP TABLE if EXISTS salesdetail;
DROP TABLE if EXISTS customer;
DROP TABLE if EXISTS item;

CREATE TABLE item(
	itemID INT NOT NULL AUTO_INCREMENT,
	itemcode VARCHAR(10) NOT NULL UNIQUE,
	iname VARCHAR(100),
	unitprice INT,
	maker VARCHAR(50),
	lastupdate DATETIME,
	PRIMARY KEY(itemID)
);

CREATE TABLE customer(
	customerID INT NOT NULL AUTO_INCREMENT,
	cname VARCHAR(50),
	caddress VARCHAR(100),
	tel VARCHAR(20),
	lastupdate DATETIME,
	PRIMARY KEY(customerID)
);

CREATE TABLE salesdetail(
	salesdetailID INT NOT NULL AUTO_INCREMENT,
	itemcode VARCHAR(100),
	customerID INT,
	quantity INT,
	salesdate DATE,
	lastupdate DATETIME,
	PRIMARY KEY(salesdetailID),
	FOREIGN KEY(itemcode)
		REFERENCES item(itemcode)
			ON DELETE CASCADE
			ON UPDATE CASCADE,
	FOREIGN KEY(customerID)
		REFERENCES customer(customerID)
			ON DELETE CASCADE
			ON UPDATE CASCADE
);

DESC item;
DESC customer;
DESC salesdetail;