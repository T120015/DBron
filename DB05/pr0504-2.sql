-- 6)
SELECT kinmu_employee.l_name, kinmu_employee.f_name, AVG(kinmu_timecard.work_time) AS kinmuheikin
FROM kinmu_timecard
INNER JOIN kinmu_employee
ON kinmu_timecard.s_id = kinmu_employee.s_id
GROUP BY kinmu_employee.s_id
ORDER BY kinmuheikin
;

-- 7)
SELECT kinmu_employee.l_name, kinmu_employee.f_name, AVG(kinmu_timecard.work_time) AS kinmuheikin
FROM kinmu_timecard
RIGHT JOIN kinmu_employee
ON kinmu_timecard.s_id = kinmu_employee.s_id
GROUP BY kinmu_employee.s_id
ORDER BY kinmuheikin
;