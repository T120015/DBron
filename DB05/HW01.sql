USE dbron05;

-- 1)
SELECT *
FROM seiseki
INNER JOIN gakuseki
ON seiseki.gakusekiID = gakuseki.gakusekiID
WHERE season = 2018
;

-- 2)
SELECT *
FROM seiseki
INNER JOIN gakuseki
ON seiseki.gakusekiID = gakuseki.gakusekiID
WHERE season = 2018
AND seiseki.kamoku = '数学'
;

-- 3)
SELECT gakuseki.gakusekiID, namae, SUM(score) AS goukei
FROM seiseki
INNER JOIN gakuseki
ON seiseki.gakusekiID = gakuseki.gakusekiID
GROUP BY gakusekiID
;

-- 4)
SELECT gakuseki.gakusekiID, namae, SUM(score) AS goukei
FROM seiseki
INNER JOIN gakuseki
ON seiseki.gakusekiID = gakuseki.gakusekiID
WHERE season = 2018
GROUP BY gakusekiID
;

-- 5)
SELECT ggteacher, AVG(score) AS heikin
FROM seiseki
INNER JOIN gakuseki
ON seiseki.gakusekiID = gakuseki.gakusekiID
GROUP BY ggteacher
;

-- 6)
SELECT ggteacher, AVG(score) AS heikin
FROM seiseki
INNER JOIN gakuseki
ON seiseki.gakusekiID = gakuseki.gakusekiID
WHERE seiseki.season = 2018
GROUP BY ggteacher
;