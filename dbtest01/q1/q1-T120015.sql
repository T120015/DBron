-- 問題1　q1-[GAKUSEKI].sql

-- (1)
USE sampledb;
SELECT *
FROM quest
WHERE prefecture = '東京都'
AND gender = '男'
;

-- (2)
SELECT * FROM post_area
WHERE city IN ('茅野市','諏訪市')
and prefecture = '長野県'
;

-- (3)
SELECT city, COUNT(city) as pcnt
from post_area
WHERE city IN ('茅野市','諏訪氏')
GROUP BY city
;

-- (4)
SELECT * FROM uri_sales
INNER JOIN uri_shop
on uri_sales.s_id = uri_shop.s_id
;

-- (5)
DROP VIEW if EXISTS shop_sales;
CREATE VIEW shop_sales as
   SELECT
        uri_shop.s_id as s_id,
        uri_shop.s_name as s_name,
        uri_sales.s_date as s_date,
        uri_sales.s_value as s_value
    FROM uri_sales
    inner JOIN uri_shop
    on uri_sales.s_id = uri_shop.s_id
;    

SELECT * 
FROM shop_sales
;

-- (6)
SELECT s_name, SUM(s_value) as total
FROM shop_sales
WHERE s_name LIKE ('%花町%')
GROUP BY s_name
;
