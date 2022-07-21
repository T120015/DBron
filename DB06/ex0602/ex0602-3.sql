-- ex0602-3.sql

USE dbron06;

DROP VIEW if exists gaku_sei;

CREATE VIEW gaku_sei as 
    

select *
FROM gaku_sei
WHERE gcode = 'H001'
;
