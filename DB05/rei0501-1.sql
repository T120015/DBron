-- 1)
SELECT l_name, f_name, gender, kinmu_depart.depart_id, kinmu_depart.depart_name, class
FROM kinmu_employee
LEFT JOIN kinmu_depart
ON kinmu_employee.depart_id = kinmu_depart.depart_id
;

-- 2)
SELECT l_name, f_name, gender, kinmu_depart.depart_id, kinmu_depart.depart_name, class
FROM kinmu_employee
RIGHT JOIN kinmu_depart
ON kinmu_employee.depart_id = kinmu_depart.depart_id
;