USE sampledb;

-- 1)
SELECT *
FROM kinmu_timecard
INNER JOIN kinmu_employee
ON kinmu_timecard.s_id = kinmu_employee.s_id
;

-- 2)
SELECT kinmu_employee.s_id, kinmu_employee.l_name, kinmu_employee.f_name, r_date, work_time, kinmu_employee.gender, kinmu_employee.class
FROM kinmu_timecard
INNER JOIN kinmu_employee
ON kinmu_timecard.s_id = kinmu_employee.s_id
;

-- 3)
SELECT kinmu_employee.s_id, kinmu_employee.l_name, kinmu_employee.f_name, r_date, work_time, kinmu_employee.gender, kinmu_employee.class
FROM kinmu_timecard
INNER JOIN kinmu_employee
ON kinmu_timecard.s_id = kinmu_employee.s_id
ORDER BY kinmu_employee.s_id, r_date
;

-- 4)
SELECT kinmu_employee.s_id, kinmu_employee.l_name, kinmu_employee.f_name, r_date, work_time, kinmu_employee.gender, kinmu_employee.class
FROM kinmu_timecard
INNER JOIN kinmu_employee
ON kinmu_timecard.s_id = kinmu_employee.s_id
WHERE kinmu_employee.gender = 2
ORDER BY kinmu_employee.s_id, r_date
;

-- 5)
SELECT po_id, e_usr.user_id, e_usr.l_name, e_usr.f_name, e_usr.prefecture, order_date
FROM e_ordermain
INNER JOIN e_usr
ON e_ordermain.user_id = e_usr.user_id
;

-- 6)
SELECT po_id, e_usr.user_id, e_usr.l_name, e_usr.f_name, e_usr.prefecture, order_date
FROM e_ordermain
INNER JOIN e_usr
ON e_ordermain.user_id = e_usr.user_id
WHERE e_usr.prefecture IN ('東京都','栃木県')
;

-- 7)
SELECT po_id, e_usr.user_id, e_usr.l_name, e_usr.f_name, e_usr.prefecture, order_date
FROM e_ordermain
INNER JOIN e_usr
ON e_ordermain.user_id = e_usr.user_id
WHERE e_usr.prefecture IN ('東京都','栃木県')
AND order_date LIKE ('2004%')
;

-- 8)
SELECT uri_shop.s_id, uri_shop.s_name, s_date, s_value
FROM uri_sales
INNER JOIN uri_shop
ON uri_sales.s_id = uri_shop.s_id
ORDER BY uri_shop.s_id
;