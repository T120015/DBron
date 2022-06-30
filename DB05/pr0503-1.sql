-- 1)
SELECT e_ordermain.user_id, e_ordermain.order_date, e_ordermain.delivery_date, e_product.p_name, e_product.price, e_orderdetail.quantity
FROM e_orderdetail
INNER JOIN e_product
ON e_orderdetail.p_id = e_product.p_id
INNER JOIN e_ordermain
ON e_orderdetail.po_id = e_ordermain.po_id
;

-- 2)
SELECT e_ordermain.user_id, e_ordermain.order_date, e_ordermain.delivery_date, e_product.p_name, e_product.price, e_orderdetail.quantity
FROM e_orderdetail
INNER JOIN e_product
ON e_orderdetail.p_id = e_product.p_id
INNER JOIN e_ordermain
ON e_orderdetail.po_id = e_ordermain.po_id
WHERE e_ordermain.order_date >= '2005-01-01'
AND e_ordermain.order_date < '2005-07-01'
;

-- 3)
SELECT e_usr.user_id, e_ordermain.order_date, e_ordermain.delivery_date, e_product.p_name, e_product.price, e_orderdetail.quantity
FROM e_orderdetail
INNER JOIN e_product
ON e_orderdetail.p_id = e_product.p_id
INNER JOIN e_ordermain
ON e_orderdetail.po_id = e_ordermain.po_id
INNER JOIN e_usr
ON e_ordermain.user_id = e_usr.user_id
;
