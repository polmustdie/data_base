SELECT * FROM violation_types WHERE max_sanction = 5000;
SELECT * FROM violation_types WHERE max_sanction >= 5000;
SELECT * FROM violation_types WHERE max_sanction > 5000;
SELECT * FROM violation_types ORDER BY violation_type DESC LIMIT 3;
SELECT * FROM violation_types ORDER BY max_sanction ASC LIMIT 4;

SELECT * FROM drivers WHERE name LIKE 'I_';
SELECT * FROM drivers WHERE name LIKE 'S%';
SELECT * FROM drivers WHERE date_of_birth LIKE '%2000';
SELECT DISTINCT date_of_birth, name FROM drivers LIMIT 2;
SELECT DISTINCT date_of_birth, name FROM drivers;

SELECT * FROM violations WHERE violation_date = '12.09.2022';
SELECT * FROM violations WHERE violation_date LIKE '%202_';
SELECT DISTINCT violation_date, violation_type_id FROM violations
    ORDER BY violation_type_id;
SELECT DISTINCT violation_date FROM violations;

SELECT * FROM cars WHERE model IS NOT NULL;
SELECT DISTINCT model FROM cars;
SELECT DISTINCT model, color FROM cars LIMIT 4;
SELECT * FROM cars WHERE id_driver = '4402192234';
SELECT * FROM cars WHERE id_driver = '4402194455';

SELECT * FROM violation_per_driver ORDER BY violation_id ASC;
SELECT DISTINCT driver_id FROM violation_per_driver;
SELECT * FROM violation_per_driver;
SELECT * FROM violation_per_driver LIMIT 2;
SELECT * FROM violation_per_driver WHERE driver_id LIKE '4%';

-- LABA 3

--размер штрафов для каждого водителя

SELECT drivers.name, SUM(max_sanction) FROM violation_types, violations, violation_per_driver, drivers
     WHERE drivers.id = violation_per_driver.driver_id AND violations.id = violation_per_driver.violation_id
       AND violation_type = violations.violation_type_id GROUP BY drivers.name;

--водители соверш более 3 различных нарушений

SELECT driver_id, COUNT(violation_id), drivers.name FROM violation_per_driver, drivers
                WHERE drivers.id = violation_per_driver.driver_id GROUP BY driver_id, drivers.name
                                                        HAVING COUNT(DISTINCT violation_id) >= 3 ;

--виды нарушений, по которым общая сумма штрафов > 10000

SELECT violation_description,COUNT(violation_type_id) * max_sanction FROM violation_types, violations
    WHERE violation_type = violations.violation_type_id GROUP BY violation_description, max_sanction
                    HAVING COUNT(violation_type_id) * max_sanction > 10000;

--LABA 4

/*Определить водителей, имеющих в своем активе штрафов на сумму
больше средней суммы всех уплаченных*/

SELECT drivers.name, SUM(max_sanction) FROM violation_types, violations, violation_per_driver, drivers
     WHERE drivers.id = violation_per_driver.driver_id AND violations.id = violation_per_driver.violation_id
     AND violation_type = violations.violation_type_id GROUP BY drivers.name
     HAVING SUM(max_sanction) > (SELECT AVG(max_sanction) FROM violation_types);

/*Определить виды нарушений, для которых общая сумма не превышает
средней*/

SELECT violation_description,COUNT(violation_type_id) * max_sanction FROM violation_types, violations
    WHERE violation_type = violations.violation_type_id GROUP BY violation_description, max_sanction
    HAVING COUNT(violation_type_id) * max_sanction <= (SELECT AVG(max_sanction) FROM violation_types);

/*Определить число водителей для каждого типа нарушения, по которым
уплаченная сумма выше средней*/

SELECT violation_description, COUNT(DISTINCT driver_id) FROM violation_types, drivers, violations, violation_per_driver
WHERE violation_type = violations.violation_type_id AND drivers.id =  violation_per_driver.driver_id
AND violations.id = violation_per_driver.violation_id GROUP BY violation_description, max_sanction
HAVING COUNT(violation_type_id) * max_sanction > (SELECT AVG(max_sanction) FROM violation_types);

--LABA 5

/* Вывести типы штрафов, по которым нет ни одного нарушения
*/
SELECT violation_description FROM violation_types
    LEFT JOIN violations ON violation_type = violations.violation_type_id
    WHERE violation_type_id IS NULL;
/*
  Вывести водителей с указанием количества нарушений или написать "нет", если нарушений не было   */
SELECT name, cast(count(violation_id) as char(15)) FROM drivers, violation_per_driver
    WHERE drivers.id = violation_per_driver.driver_id GROUP BY name
UNION
SELECT name, 'нет' AS count_drivers
    FROM drivers
    LEFT JOIN violation_per_driver vpd ON drivers.id = vpd.driver_id
    WHERE violation_id IS NULL;
/*
Определить перечень нарушений с указанием их количества, которые состоялись 1.04.2019
*/
SELECT violation_description, COUNT(violations.violation_type_id) FROM violation_types
    LEFT JOIN violations ON violation_type = violations.violation_type_id
    WHERE violations.violation_date = '01.04.2019'
    GROUP BY violation_description;





