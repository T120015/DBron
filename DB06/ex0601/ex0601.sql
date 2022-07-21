-- 例題0601　ex0601-1.sql
use sampledb;

-- (1)
#もし，viewが存在したら，削除する
DROP VIEW if exists emp_dep;
# ビューemp_depを新規作成CREATE VIEW 
CREATE VIEW emp_dep AS 
	SELECT
		kinmu_employee.s_id AS s_id,
		kinmu_employee.l_name AS l_name,
		kinmu_employee.f_name AS f_name,
		kinmu_employee.gender AS gender,
		kinmu_employee.class AS class,
		kinmu_depart.depart_id AS depart_id,
		kinmu_depart.depart_name AS depart_name
	FROM kinmu_employee
	INNER JOIN kinmu_depart
	ON kinmu_employee.depart_id = kinmu_depart.depart_id
;

-- (2)
#ビューemp_depを使って，男性で部長の社員一覧
SELECT *
FROM emp_dep
WHERE gender = 1
AND class = '部長'
;

-- (3)
#ビューemp_dep_timeを作成する
#もし，viewが存在したら，削除する
DROP VIEW if exists emp_dep_time;
# ビューemp_depを新規作成CREATE VIEW 
CREATE VIEW emp_dep_time AS 
	SELECT
		kinmu_employee.s_id AS s_id,
		kinmu_employee.l_name AS l_name,
		kinmu_employee.f_name AS f_name,
		kinmu_employee.gender AS gender,
		kinmu_employee.class AS class,
		kinmu_depart.depart_id AS depart_id,
		kinmu_depart.depart_name AS depart_name,
		kinmu_timecard.r_date AS r_date,
		kinmu_timecard.work_time AS work_time
	FROM kinmu_timecard
	INNER JOIN kinmu_employee
	ON kinmu_timecard.s_id = kinmu_employee.s_id
	INNER JOIN kinmu_depart
	ON kinmu_employee.depart_id = kinmu_depart.depart_id
	
;


-- (4) 
#ビューemp_dep_timeを使って，社員の氏名が「木村一郎」の勤務状況を表示
SELECT *
FROM emp_dep_time
WHERE l_name = '木村'
AND f_name = '一郎'
;

-- (5)
#ビューemp_dep_timeを使って，社員の氏名が「木村一郎」の2005年11月の作業時間合計をフィールド名work200511として表示
SELECT l_name, f_name, SUM(work_time) AS WORK200511
SELECT *
FROM emp_dep_time
WHERE l_name = '木村'
AND f_name = '一郎'
AND 

-- (6)
#ビューemp_dep_timeを使って，全社員の2005年11月の作業時間合計をフィールド名work200511として集計

