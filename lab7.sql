/*Создать процедуру, вставляющую записи через первое представление из предыдущего задания.
Вставить как минимум 2 записи (т.е. вызвать процедуру дважды).*/
  CREATE PROCEDURE insert_data(a char(15), b char(15), c char(15))
LANGUAGE sql
AS $$
    INSERT INTO c_v (car_vin, color, id_driver)  VALUES (a, b, c);
$$;

CALL insert_data('111122222344', 'brown', '4601192234');
CALL insert_data('201122222344', 'magenta', '5645773398');

/*
Получить результат, формируемый
третьим представлением (предыдущего задания) через выполнение нескольких запросов,
объединённых в процедуру.
Stored procedures aren't meant to return anything, use a function*/

CREATE OR REPLACE FUNCTION my_cursor()
  RETURNS TABLE(driver_name text, c1 int, c2 int) AS
$func$
DECLARE
    d_name text;
BEGIN
    RETURN QUERY
    SELECT name as driver_name, cast(COUNT(violation_id) as integer)as c1,
    cast(COUNT(DISTINCT violation_type_id)as integer) as c2 FROM drivers
LEFT JOIN violation_per_driver vpd ON drivers.id = vpd.driver_id
LEFT JOIN violations v ON vpd.violation_id = v.id
LEFT JOIN violation_types vt ON v.violation_type_id = vt.violation_type
GROUP BY name ORDER  BY name DESC;
END
$func$ LANGUAGE plpgsql;

select * from my_cursor();



count_viol = (select f_c.count_violations from (SELECT drivers_view.name, drivers_view.c1 as count_violations FROM drivers_view
GROUP BY drivers_view.name, drivers_view.c1)as f_c where driver_name=f_c.name);
count_d_viol = (select f_c.count_d_violations from (SELECT drivers_view.name, drivers_view.c2 as count_d_violations FROM drivers_view
GROUP BY drivers_view.name, drivers_view.c1, drivers_view.c2)as f_c where driver_name=f_c.name);


select drivers.name, count(violations) from drivers, violations, violation_per_driver
where drivers.id = violation_per_driver.driver_id and violation_per_driver.violation_id = violations.id
group by drivers.name;
/*СЮДААААА*/

CREATE OR REPLACE FUNCTION get_violations(name_driver out text, count_violations out int,
                                                    count_d_violations out int)
RETURNS SETOF record AS $$
DECLARE
count_viol int default 0;
count_d_viol int default 0;
driver_name text;
driver_cursor cursor FOR SELECT drivers.name FROM drivers;

BEGIN
    CREATE TEMPORARY TABLE IF NOT EXISTS temp_table (name_driver text, count_violations int,
                                                    count_d_violations int);
    OPEN driver_cursor;
    LOOP
        FETCH driver_cursor INTO driver_name;
        EXIT WHEN NOT FOUND;
        count_viol = (SELECT COUNT(violation_id) FROM drivers
        LEFT JOIN violation_per_driver vpd ON drivers.id = vpd.driver_id and driver_name = drivers.name
        LEFT JOIN violations v ON vpd.violation_id = v.id
        LEFT JOIN violation_types vt ON v.violation_type_id = vt.violation_type);
        count_d_viol = (SELECT COUNT(distinct violation_type_id) FROM drivers
        LEFT JOIN violation_per_driver vpd ON drivers.id = vpd.driver_id and driver_name = drivers.name
        LEFT JOIN violations v ON vpd.violation_id = v.id
        LEFT JOIN violation_types vt ON v.violation_type_id = vt.violation_type);
        INSERT INTO temp_table VALUES(driver_name, count_viol, count_d_viol);
    END LOOP;
    CLOSE driver_cursor;
    RETURN QUERY SELECT * FROM temp_table;
    drop table temp_table;
END; $$
LANGUAGE plpgsql;


select * from get_violations();
/*Создать процедуру с параметром по умолчанию и выходным параметром.*/

CREATE FUNCTION test(out a integer, d_id char(15) default '5645773398')
    RETURNS integer
AS $$
DECLARE
	  cr1 CURSOR FOR SELECT SUM(max_sanction) FROM violation_types, violations, violation_per_driver, drivers
     WHERE drivers.id = violation_per_driver.driver_id and drivers.id = d_id
       AND violations.id = violation_per_driver.violation_id
       AND violation_type = violations.violation_type_id GROUP BY drivers.name;
	  s real := 0.0;
	  mk integer;
BEGIN
	  OPEN cr1;
	  LOOP
	     FETCH cr1 INTO mk;
	     IF NOT FOUND THEN EXIT;END IF;
	  s := s + mk;
	  END LOOP;
	  CLOSE cr1;
	  a := s;
END;
$$
LANGUAGE plpgsql;

select * from test('4601192234');


