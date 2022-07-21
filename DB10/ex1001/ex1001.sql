CREATE DATABASE if NOT EXISTS dbron10;
USE dbron10;

DROP table if exists fishbook;
CREATE TABLE fishbook(
	fishbookID INT NOT NULL AUTO_INCREMENT,
	filename VARCHAR(100),
	mime VARCHAR(100),
	bikou VARCHAR(200),
	filesize INT ,
	imagefile mediumBLOB ,
	PRIMARY KEY(fishbookID)
);
DESC fishbook;
