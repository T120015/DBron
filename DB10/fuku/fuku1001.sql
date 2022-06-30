--fuku1001.sql
use sampledb;

--(1)
SELECT *
FROM quest
WHERE prefecture LIKE ('%東京%')
;

--(2)
SELECT prefecture, COUNT(prefecture) AS cnt
FROM quest
GROUP BY prefecture
;

--(3)
SELECT *
FROM kinmu_employee
INNER JOIN kinmu_depart
    ON kinmu_employee.depart_id = kinmu_depart.depart_id
;

--(4)
SELECT kinmu_employee.l_name, kinmu_employee.f_name, kinmu_employee.class, kinmu_depart.depart_name, SUM(kinmu_timecard.work_time) AS k_total
from kinmu_timecard
INNER JOIN kinmu_employee
    on kinmu_timecard.s_id = kinmu_employee.s_id
INNER JOIN kinmu_depart
    on kinmu_employee.depart_id = kinmu_depart.depart_id
GROUP BY kinmu_employee.s_id
;

--(5)


--(6)


