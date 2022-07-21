-- pr0602-2.sql 3つのテーブルを内部結合するビュー
USE dbron06;

DROP VIEW if EXISTS item_cus_sal;

CREATE VIEW item_cus_sal AS 
	SELECT
		customer.customerID AS customerID,
		customer.cname AS cname,
		item.iname AS iname,
		item.unitprice AS unitprice,
		salesdetail.quantity AS quantity,
		item.unitprice * salesdetail.quantity AS price,
		salesdetail.salesdate AS salesdate
	FROM salesdetail
	INNER JOIN customer
	ON salesdetail.customerID = customer.customerID
	INNER JOIN item
	ON salesdetail.itemcode = item.itemcode
;