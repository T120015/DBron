CREATE DATABASE if NOT EXISTS dbron;
USE dbron;

DROP TABLE if EXISTS pickup;
DROP TABLE if EXISTS koudou_friend;
DROP TABLE if EXISTS koudou_shosai;
DROP TABLE if EXISTS kansatu;
DROP TABLE if EXISTS koudou;
DROP TABLE if EXISTS corona;
DROP TABLE if EXISTS client;
DROP TABLE if EXISTS school;

CREATE TABLE school(
	schoolID INT NOT NULL AUTO_INCREMENT,
	position VARCHAR(10),
	class VARCHAR(10),
	lastupdate DATETIME DEFAULT NOW(),
	delflag BOOL DEFAULT FALSE,
	PRIMARY KEY (schoolID) 
);

CREATE TABLE client(
	clientID INT NOT NULL AUTO_INCREMENT,
	schoolID INT,
	clientcode VARCHAR(10) UNIQUE,
	pass VARCHAR(20),
	namae VARCHAR(30),
	age INT,
	gender VARCHAR(10),
	phone VARCHAR(15),
	email VARCHAR(50),
	faculty VARCHAR(30),
	lastupdate DATETIME DEFAULT NOW(),
	delflag BOOL DEFAULT FALSE,
	PRIMARY KEY (clientID),
	FOREIGN KEY(schoolID)
		REFERENCES school(schoolID)
		ON UPDATE CASCADE
		ON DELETE CASCADE
); 


CREATE TABLE kansatu(
	kansatuID INT NOT NULL AUTO_INCREMENT,
	clientcode VARCHAR(10),
	record DATE,
	meridiem VARCHAR(10),
	temp FLOAT,
	pain BOOL,
	feeling BOOL,
	headache BOOL,
	throat BOOL,
	breathness BOOL,
	cough BOOL,
	nausea BOOL,
	diarrhea BOOL,
	taste BOOL,
	olfactory BOOL,
	lastupdate DATETIME DEFAULT NOW(),
	delflag BOOL DEFAULT FALSE,
	PRIMARY KEY (kansatuID),
	FOREIGN KEY(clientcode)
		REFERENCES client(clientcode)
		ON UPDATE CASCADE
		ON DELETE CASCADE	
);

CREATE TABLE koudou(
	koudouID INT NOT NULL AUTO_INCREMENT,
	clientcode VARCHAR(10),
	action DATE,
	start TIME,
	end TIME,
	location VARCHAR(30),
	move VARCHAR(10),
	departure VARCHAR(20),
	arrival VARCHAR(20),
	companions BOOL,
	lastupdate DATETIME DEFAULT NOW(),
	delflag BOOL DEFAULT FALSE,
	PRIMARY KEY (koudouID),
	FOREIGN KEY(clientcode)
		REFERENCES client(clientcode)
		ON UPDATE CASCADE
		ON DELETE CASCADE
);

CREATE TABLE koudou_shosai(
	shosaiID INT NOT NULL AUTO_INCREMENT,
	koudouID INT,
	who VARCHAR(20),
	people_num INT,
	remarks VARCHAR(50),
	lastupdate DATETIME DEFAULT NOW(),
	delflag BOOL DEFAULT FALSE,
	PRIMARY KEY (shosaiID),
	FOREIGN KEY(koudouID)
		REFERENCES koudou(koudouID)
		ON UPDATE CASCADE
		ON DELETE CASCADE
);

CREATE TABLE koudou_friend(
	friendID INT NOT NULL AUTO_INCREMENT,
	shosaiID INT,
	friendcode VARCHAR(10),
	PRIMARY KEY(friendID),
	FOREIGN KEY(shosaiID)
		REFERENCES koudou_shosai(shosaiID)
		ON UPDATE CASCADE
		ON DELETE CASCADE
);

CREATE TABLE corona(
	coronaID INT NOT NULL AUTO_INCREMENT,
	clientcode VARCHAR(10),
	judge BOOL,
	onset DATE,
	stopflag BOOL,
	lastupdate DATETIME DEFAULT NOW(),
	delflag BOOL DEFAULT FALSE,
	PRIMARY KEY (coronaID),
	FOREIGN KEY(clientcode)
		REFERENCES client(clientcode)
		ON UPDATE CASCADE
		ON DELETE CASCADE
);

CREATE TABLE pickup(
	pickupID INT NOT NULL AUTO_INCREMENT,
	clientcode VARCHAR(10),
	pickupflag INT,
	lastupdate DATETIME DEFAULT NOW(),
	delflag BOOL DEFAULT FALSE,
	PRIMARY KEY (pickupID),
	FOREIGN KEY(clientcode)
		REFERENCES client(clientcode)
		ON UPDATE CASCADE
		ON DELETE CASCADE
);

DESC client;
DESC school;
DESC kansatu;
DESC koudou;
DESC koudou_shosai;
DESC koudou_friend;
DESC corona;
DESC pickup;