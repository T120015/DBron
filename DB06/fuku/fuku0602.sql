-- (2)
-- データベースを新規作成
CREATE DATABASE if not EXISTS dbron06;
use dbron06;
-- もし既に存在する場合は，テーブル削除　
-- 順番に注意！外部キーがあるテーブルから削除する
DROP TABLE if EXISTS uriage;
DROP TABLE if EXISTS customer;

-- テーブル作成　
-- 順番に注意！ 外部キーのあるテーブルがあと
CREATE TABLE customer(
    customerID int not NULL auto_increment,
    namae varchar(30),
    c_address varchar(50),
    tel varchar(20),
    
    tantou varchar(30),
    PRIMARY KEY(customerID)
);

CREATE TABLE uriage(
    uriageID int not NULL auto_increment,
    customerID int,
    uriagegaku int,
    uriagedate DATE,
    PRIMARY key(uriageID),
    FOREIGN key (customerID)
        REFERENCES customer(customerID)
        on delete CASCADE
        on update CASCADE
);

desc customer;
desc uriage;
-- レコード挿入
-- 順番に注意！外部キーのあるテーブルがあと
INSERT INTO customer
    (namae,c_address,tel,tantou)
    VALUES
    ('諏訪理科商店', '長野県茅野市豊平5000-1', '0266-63-1467', '広瀬'),
    ('東京理科商会', '新宿区神楽坂1-5-1', '03-2600-4271', '尾崎'),
    ('長万部支社', '北海道長万部町', '011-033-1234', '土屋')
;

insert into uriage
    (customerID,uriagegaku,uriagedate)
    VALUES
    (1,2000,'2022/5/1'),
    (1,3500,'2022/5/3'),
    (1,2300,'2022/5/4'),
    (2,5000,'2022/5/2'),
    (2,10000,'2022/5/7'),
    (3,3000,'2022/5/3')
;
select *
FROM uriage
inner join customer
on uriage.customerID = customer.customerID
;

