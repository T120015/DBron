-- fuku0701.sql
-- (1) 
USE sampledb;

DROP VIEW if EXISTS shop_sales;
CREATE VIEW shop_sales AS 
	SELECT
		uri_shop.s_id AS s_id,
		uri_shop.s_name AS s_name,
		uri_sales.s_date AS s_date,
		uri_sales.s_value AS s_value
	FROM uri_sales
	INNER JOIN uri_shop
	ON uri_sales.s_id = uri_shop.s_id
;

SELECT * 
FROM shop_sales;

-- (2)
SELECT s_id, s_name, SUM(s_value) AS goukei
FROM shop_sales
GROUP BY s_id
;

-- (3)
SELECT s_date, SUM(s_value) AS goukei
FROM shop_sales
GROUP BY s_date
;
