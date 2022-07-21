use dbron;
DROP view if exists koudou_all;
CREATE view koudou_all AS
    SELECT
        client.clientID as clientID,
        koudou.koudouID AS koudouID,
        koudou_shosai.shosaiID AS shosaiID,
        koudou_friend.friendID AS friendID,
        client.clientcode AS clientcode,
        client.namae AS namae,
        client.age AS age,
        client.gender AS gender,
        client.faculty AS faculty,
        school.`position` AS `position`,
        school.class AS class,
        koudou.`action` AS `action`,
        koudou.`start` AS `start`,
        koudou.`end` AS `end`,
        koudou.location AS location,
        koudou.move AS move,
        koudou.departure AS departure,
        koudou.arrival AS arrival,
        koudou.companions AS companions,
        koudou_shosai.who AS who,
        koudou_shosai.people_num AS people_num,
        koudou_shosai.remarks AS remarks,
        koudou_friend.friendcode AS friendcode,
        koudou.lastupdate AS lastupdate,
        koudou.delflag as delflag
    FROM koudou_friend
    RIGHT JOIN koudou_shosai
    ON koudou_friend.shosaiID = koudou_shosai.shosaiID
    RIGHT JOIN koudou
    ON koudou_shosai.koudouID = koudou.koudouID
    INNER JOIN client
    ON koudou.clientcode = client.clientcode
    INNER JOIN school
    ON client.schoolID = school.schoolID
;