-- 1)
SELECT kinmu_employee.l_name, kinmu_employee.f_name, kinmu_employee.gender, r_date, work_time, kinmu_employee.class
FROM kinmu_timecard
RIGHT JOIN kinmu_employee
ON kinmu_timecard.s_id = kinmu_employee.s_id
;

-- 2)
SELECT kinmu_employee.l_name, kinmu_employee.f_name, kinmu_employee.gender, r_date, work_time, kinmu_employee.class
FROM kinmu_timecard
LEFT JOIN kinmu_employee
ON kinmu_timecard.s_id = kinmu_employee.s_id
;

-- 3)
SELECT po_id, e_usr.user_id, e_usr.l_name, e_usr.f_name, e_usr.prefecture, order_date
FROM e_ordermain
LEFT JOIN e_usr
ON e_ordermain.user_id = e_usr.user_id
;

-- 4)
SELECT ac_menu.page_id, ac_menu.title, ip_address, access_date
FROM ac_accesslog
RIGHT JOIN ac_menu
ON ac_accesslog.page_id = ac_menu.page_id
;

-- 5)
SELECT ac_menu.page_id, ac_menu.title, ip_address, access_date
FROM ac_accesslog
RIGHT JOIN ac_menu
ON ac_accesslog.page_id = ac_menu.page_id
WHERE access_date LIKE ('2005-12%')
;

-- 6)
SELECT *
FROM bo_books
LEFT JOIN bo_category
ON bo_books.category_id = bo_category.category_id
;
