-- q33
use dbtest01;

DROP VIEW if EXISTS ga_ka_at;

CREATE VIEW ga_ka_at as 
    SELECT 
        gakuseki.gakusekiID as gakusekiID,
        gakuseki.gakusekicode as gakusekicode,
        gakuseki.namae as namae,
        gakuseki.a_year as a_year,
        kamoku.kamokuID as kamokuID,
        kamoku.kamokucode as kamokucode,
        kamoku.subjectname as subjectname,
        kamoku.tantou as tantou,
        attendance.attendanceID as attendanceID,
        attendance.classdate as classdate,
        attendance.atdata as atdata
    from attendance
    INNER JOIN gakuseki
    on attendance.gakusekicode = gakuseki.gakusekicode
    INNER JOIN kamoku
    on attendance.kamokucode = kamoku.kamokucode
;

SELECT * FROM ga_ka_at;
    

