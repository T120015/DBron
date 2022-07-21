-- 演習１　pr0601.sql
USE sampledb;

-- (1)
DROP VIEW if EXISTS order_sumary;

CREATE VIEW order_sumary AS (
	SELECT
		e_usr.user_id AS user_id,
		e_usr.l_name AS l_name,
		e_usr.f_name AS f_name,
		e_ordermain.order_date AS order_date,
		e_product.p_name AS p_name,
		e_product.price AS price,
		e_orderdetail.quantity AS quantity,
		e_product.price * e_orderdetail.quantity AS s_total
	FROM e_orderdetail
	INNER JOIN e_ordermain
	ON e_orderdetail.po_id = e_ordermain.po_id
	INNER JOIN e_product
	ON e_orderdetail.p_id = e_product.p_id
	INNER JOIN e_usr
	ON e_ordermain.user_id = e_usr.user_id
);

-- (2)
SELECT *
FROM order_sumary
;


-- (3)
SELECT user_id, l_name, f_name, SUM(s_total) AS goukei
FROM order_sumary
GROUP BY user_id
;

