-- 問題２(1)

CREATE DATABASE IF NOT EXISTS dbtest01;

USE dbtest01;

DROP TABLE if EXISTS uriage;
CREATE TABLE uriage(
    uriageID INT NOT NULL AUTO_INCREMENT,
    tantou VARCHAR(30) NOT NULL,
    area VARCHAR(30) NOT NULL,
    sales INT NOT NULL,
    s_date date,
    PRIMARY KEY (uriageID)
)
;

DESC uriage;


