-- 9)
SELECT ac_menu.page_id, ac_menu.title, ip_address, access_date
FROM ac_accesslog
INNER JOIN ac_menu
ON ac_accesslog.page_id = ac_menu.page_id
;

-- 10)
SELECT ac_menu.page_id, ac_menu.title, ip_address, access_date
FROM ac_accesslog
INNER JOIN ac_menu
ON ac_accesslog.page_id = ac_menu.page_id
WHERE access_date LIKE ('2005-11%')
;

-- 11)
SELECT *
FROM bo_books
INNER JOIN bo_category
ON bo_books.category_id = bo_category.category_id
;