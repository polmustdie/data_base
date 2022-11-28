/*
Создать процедуру и триггеры (в том числе триггер, вызывающий процедуру) по варианту,
а также разработать небольшое приложение, связывающееся с разработанной БД.
Из приложения осуществить вставку (удаление или изменение) данных, влекущую запуск триггера,
осуществить вызов хранимой процедуры, а также осуществить выполнение набора команд (нескольких запросов)
в виде единого пакета (транзакции) с откатом в случае, если хотя бы одна из этих операций завершится неудачно.*/

 /*
Разработать процедуру, выводящую водителей и автомобили (со всеми характеристиками)
  совершившие определенное нарушение в заданный временной период
*/

CREATE OR REPLACE FUNCTION func8(start_ date, end_ date, v_id integer)
  RETURNS TABLE(driver_id varchar(10), driver_name text, driver_d_o_b varchar(10),
  car_id varchar(15), car_color varchar(15), car_model varchar(15), v_date date) AS
$func$
BEGIN
    RETURN QUERY
    SELECT drivers.id, drivers.name, drivers.date_of_birth, car_vin, color, model, violation_date
FROM drivers, cars,violations, violation_per_driver, violation_types
     WHERE drivers.id = cars.id_driver and violations.violation_date >= start_ and
           violations.violation_date <= end_ and violations.violation_type_id = v_id
       and violations.id = violation_per_driver.violation_id
     and violations.id = violation_per_driver.violation_id
     and violation_per_driver.driver_id = drivers.id and violations.car_id = cars.car_vin
           GROUP BY drivers.id, drivers.name, car_vin, violation_date;
END
$func$ LANGUAGE plpgsql;

select * from func8('2022-11-22', '2022-11-25', 1);
/*
Разработать триггер на добавление нарушения, если не указана
  дата, то задавать текущую
*/
CREATE OR REPLACE FUNCTION update_modified_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.violation_date = now();
    RETURN NEW;
END;
$$ language plpgsql;

CREATE TRIGGER violations_trigger BEFORE
    INSERT ON violations FOR EACH ROW EXECUTE PROCEDURE  update_modified_column();

INSERT INTO violations(violation_type_id) VALUES( '1');
/*
Разработать триггер на добавление автомобиля, добавить,
  если водитель владеет не более чем 3 автомобилями, в противном случае откатить транзакцию
*/

create or replace function fn_check_cars() returns trigger as $psql$
    declare curr_car_count integer;

    begin
        curr_car_count = (select count(car_vin) from cars where id_driver = new.id_driver);
        if (curr_car_count + 1 > 3) then
            RAISE EXCEPTION 'Too many cars for this driver';
        end if;
        return new;
    end;
$psql$ language plpgsql;

create trigger check_cars before insert on cars
for each row execute procedure fn_check_cars();

INSERT INTO cars(car_vin, color, id_driver, model) VALUES('333333333336', 'red', '1933607316', 'Audi');
/*
Разработать триггер на обновление типа нарушения, обновляющий
  сумму штрафа (для обновления разработать процедуру)
  */

CREATE OR REPLACE FUNCTION update_violation()
RETURNS TRIGGER AS
$$
    BEGIN
         IF NEW.violation_description <> OLD.violation_description THEN
             UPDATE violation_types
             SET max_sanction = max_sanction+5
             where violation_type = NEW.violation_type;
         END IF;
         return new;
    END
$$
LANGUAGE plpgsql;

CREATE TRIGGER update_violation_trigger
    AFTER UPDATE
    ON violation_types FOR EACH ROW
    EXECUTE PROCEDURE update_violation();


UPDATE violation_types set violation_description = 'drunk driving updated' where violation_type = 1;


