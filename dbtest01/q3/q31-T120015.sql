-- q31
USE dbtest01;

DROP TABLE if EXISTS attendance;
DROP TABLE if EXISTS kamoku;
DROP TABLE if EXISTS gakuseki;

CREATE TABLE gakuseki(
    gakusekiID int not null AUTO_INCREMENT,
    gakusekicode VARCHAR(10) NOT NULL UNIQUE,
    namae VARCHAR(30) NOT NULL,
    a_year int not null,
    delflag boolean DEFAULT False,
    lastupdate DATETIME,
    PRIMARY KEY(gakusekiID)
);

CREATE TABLE kamoku(
    kamokuID int not null AUTO_INCREMENT,
    kamokucode VARCHAR(10) NOT NULL UNIQUE,
    subjectname VARCHAR(50) not null,
    tantou VARCHAR(30) not null,
    lastupdate DATETIME,
    PRIMARY KEY(kamokuID)
);

CREATE TABLE attendance(
    attendanceID int not null AUTO_INCREMENT,
    gakusekicode VARCHAR(10),
    kamokucode VARCHAR(10),
    classdate date not null,
    atdata int not null,
    lastupdate DATETIME,
    PRIMARY KEY(attendanceID),
    FOREIGN KEY(gakusekicode)
        REFERENCES gakuseki(gakusekicode)
        on DELETE CASCADE
        on UPDATE CASCADE,
    FOREIGN KEY(kamokucode)
        REFERENCES kamoku(kamokucode)
        on DELETE CASCADE
        on UPDATE CASCADE
);

desc gakuseki;
desc kamoku;
desc attendance;
