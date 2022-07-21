-- 問題２(2)
USE dbtest01;

DROP TABLE if EXISTS uriage;
CREATE TABLE uriage(
    uriageID INT NOT NULL AUTO_INCREMENT,
    tantou VARCHAR(30) NOT NULL,
    area VARCHAR(30) NOT NULL,
    sales INT NOT NULL,
    s_date date,
    cancelflag boolean DEFAULT False,
    lastupdate DATETIME,
    PRIMARY KEY (uriageID)
)
;
