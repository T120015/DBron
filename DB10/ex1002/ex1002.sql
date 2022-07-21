CREATE DATABASE if NOT EXISTS dbron10;
USE dbron10;

DROP table if exists fishbook2;
CREATE TABLE fishbook2(
	fishbook2ID INT NOT NULL AUTO_INCREMENT,
	filename VARCHAR(100),
	mime VARCHAR(100),
	bikou VARCHAR(200),
	filesize INT ,
	PRIMARY KEY(fishbook2ID)
);
DESC fishbook2;
