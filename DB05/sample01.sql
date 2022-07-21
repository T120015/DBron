USE dbron05;

SELECT *
FROM seiseki;

-- 1)
INSERT INTO seiseki
	(gakusekiID, season, kamoku, score)
	VALUES
	(1, 2020, 'ゼミ', 90)
;
-- 2)
-- INSERT INTO seiseki
	-- (gakusekiID, season, kamoku, score)
	-- VALUES
	-- (6, 2020, 'ゼミ', 85)
-- ;	
-- 3)
INSERT INTO gakuseki
(gakusekicode, namae, ggteacher)
	VALUES
	('H006', '魚本', '薬丸')
;
-- 4)
INSERT INTO seiseki
	(gakusekiID, season, kamoku, score)
	VALUES
	(6, 2020, 'ゼミ', 85)
;

-- 5)
UPDATE gakuseki
	SET gakusekiID = 10
	WHERE gakusekiID = 1
;

-- 6)
DELETE FROM gakuseki
WHERE gakusekiID = 2
;	