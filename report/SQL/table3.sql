use dbron;

DROP VIEW if EXISTS acount;

CREATE VIEW acount AS(
    SELECT
        client.clientID as clientID,
        school.schoolID as schoolID,
        client.clientcode as clientcode,
        school.position as position,
        school.class as class,
        client.pass as pass,
        client.namae as namae,
        client.age as age,
        client.gender as gender,
        client.phone as phone,
        client.email as email,
        client.faculty as faculty,
        client.lastupdate as lastupdate,
        client.delflag as delflag
    FROM client
    INNER JOIN school
    on school.schoolID = client.schoolID
);