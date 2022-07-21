-- データベースdbron07が存在しなければ作成
CREATE DATABASE if not EXISTS dbron07;

-- dbron07を使う
use dbron07;

-- seki,studentテーブルが既に存在すれば削除する
DROP TABLE if EXISTS seki;
DROP TABLE if EXISTS student;

-- studentテーブルの定義
CREATE TABLE student(
    studentID INT NOT NULL AUTO_INCREMENT,
    s_code VARCHAR(10) NOT NULL UNIQUE,
    namae VARCHAR(30) NOT NULL,
    prefecture VARCHAR(10),
    delflag Boolean DEFAULT False,
    lastupdate DATETIME,
    PRIMARY KEY(studentID)
);

-- sekiテーブルの定義
CREATE TABLE seki(
    sekiID INT NOT NULL AUTO_INCREMENT,
    s_code VARCHAR(10),
    jcnt INT,
    sekidata INT,
    lastupdate DATETIME,
    PRIMARY KEY(sekiID),
    FOREIGN KEY(s_code)
        REFERENCES student(s_code)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- student,sekiテーブルの説明 desc
DESC student;
DESC seki;

-- VIEW std_sekiの作成
DROP VIEW if EXISTS std_seki;
CREATE VIEW std_seki AS
    SELECT
        student.s_code AS s_code,
        student.namae AS namae,
        student.prefecture AS prefecture,
        seki.jcnt AS jcnt,
        seki.sekidata AS sekidata
    FROM seki
    INNER JOIN student
    ON seki.s_code = student.s_code
;

SELECT *
FROM std_seki;
