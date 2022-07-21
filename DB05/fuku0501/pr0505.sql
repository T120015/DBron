-- pr0501.sql 
CREATE DATABASE if NOT EXISTS dbron05;
USE dbron05;

DROP TABLE if EXISTS kamoku;
DROP TABLE if EXISTS meibo;
CREATE TABLE meibo(
    meiboID INT NOT NULL AUTO_INCREMENT,
    gakuseki VARCHAR(10) NOT NULL,
    namae VARCHAR(30) NOT NULL,
    yomi VARCHAR(50),
    acyear INT,
    birthplace VARCHAR(20),
    birthday DATE,
    PRIMARY KEY(meiboID)
);

CREATE TABLE kamoku(
	kamokuID INT NOT NULL AUTO_INCREMENT,
	meiboID INT,
	kamoku VARCHAR(20),
	instructor VARCHAR(30),
	score INT,
	PRIMARY KEY(kamokuID),
	FOREIGN KEY(meiboID)
		REFERENCES meibo(meiboID)
		ON DELETE CASCADE
		ON UPDATE CASCADE
);

DESC meibo;
DESC kamoku;

INSERT INTO meibo
(gakuseki, namae, yomi, acyear)
	VALUES
	('H001','鈴木真一','すずきしんいち',2018),
	('H002','村上健','むらかみけん',2018),
	('H003','中川勉','なかがわつとむ',2018),
	('H004','早川浩一','はやかわこういち',2018),
	('H005','高木薫','かたぎかおる',2018)
	;
	
SELECT *
FROM meibo
;

INSERT INTO kamoku
(meiboID,kamoku,score)
	VALUES
	(1,'数学',62),
	(1,'英語',56),
	(2,'数学',79),
	(2,'英語',72),
	(3,'数学',0),
	(3,'英語',15),
	(4,'数学',44),
	(4,'英語',71),
	(5,'数学',62),
	(5,'英語',44)
	;

SELECT *
FROM kamoku
;