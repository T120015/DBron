-- 1)
SELECT uri_shop.s_name, SUM(uri_sales.s_value) AS gaukei
FROM uri_sales
INNER JOIN uri_shop
ON uri_sales.s_id = uri_shop.s_id
GROUP BY uri_shop.s_name
;

-- 2)
SELECT ac_menu.title, COUNT(ac_accesslog.referer) AS kaku
FROM ac_accesslog
INNER JOIN ac_menu
ON ac_accesslog.page_id = ac_menu.page_id
GROUP BY ac_menu.title
;

-- 3)
SELECT e_usr.l_name, e_usr.f_name, COUNT(bo_rental.user_id) AS rental
FROM bo_rental
INNER JOIN e_usr
ON bo_rental.user_id = e_usr.user_id
GROUP BY e_usr.user_id
ORDER BY rental
;

-- 4)
SELECT e_usr.l_name, e_usr.f_name, COUNT(bo_rental.user_id) AS rental
FROM bo_rental
RIGHT JOIN e_usr
ON bo_rental.user_id = e_usr.user_id
GROUP BY e_usr.user_id
ORDER BY rental
;

-- 5)
SELECT bo_books.title, COUNT(bo_rental.isbn) AS rental
FROM bo_rental
RIGHT JOIN bo_books
ON bo_rental.isbn = bo_books.isbn
GROUP BY bo_books.isbn
ORDER BY rental
;