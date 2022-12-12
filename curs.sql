--Запросы

select name, drug_type, amount, price from drugs, prescriptions
where prescriptions.id_prescription = drugs.id_prescription;


select illnesses.name, drugs.name, drug_type, amount, price from drugs, prescriptions, illnesses, prescription_per_illness
where illnesses.id_illness = prescription_per_illness.illness_id
  and prescription_per_illness.prescription_id = prescriptions.id_prescription
  and prescriptions.id_prescription = drugs.id_prescription;


select clients.name, date_of_birth, drugs.name,sales.date_time_sale, sum(sales.amount_sale) from drugs
            join sales on drugs.id_drug = sales.id_drug
            join clients on sales.id_client = clients.id_client
group by drugs.name, date_of_birth, clients.name, sales.date_time_sale;


select drugs.name, sum(sales.amount_sale), date_time_sale from drugs, sales
            where drugs.id_drug = sales.id_drug
group by drugs.name, date_time_sale;


-- Представления
create view sales_per_employee as
select employees.name as emp_name, drugs.name as drug_name, sum(sales.amount_sale)*drugs.price from employees, drugs, sales
            where sales.id_employee = employees.id_employee
            and sales.id_drug = drugs.id_drug
group by employees.name, drugs.name, drugs.price;

select * from sales_per_employee;

--Процедуры
--Поставка и увеличение количества
CREATE or replace PROCEDURE update_amount(id_d int, id_s int, d_o_s date, d_amount int)
LANGUAGE plpgsql
AS
$do$
BEGIN
   if id_d  = (select drug_id from drug_per_supplier where supplier_id=id_s and drug_id=id_d) and id_s  = (select supplier_id from drug_per_supplier where supplier_id=id_s and drug_id=id_d)then
    UPDATE drugs set amount = amount + d_amount where id_drug = id_d;
    else
       insert into drug_per_supplier values(id_d, id_s, d_o_s, d_amount);
       UPDATE drugs set amount = amount + d_amount where id_drug = id_d;
       end if;
END
$do$;

CALL update_amount(1, 2, '2022-12-11', 10);

--Покупка и уменьшение количества

CREATE or replace PROCEDURE update_amount_sale(id_d int, id_e int, count_sale int, d_o_s date, id_c varchar(15))
LANGUAGE plpgsql
AS
$do$
    declare ind int = 0; --max(select id_sale from sales);
BEGIN
   ind = (select max(id_sale) from sales);
   if (select amount from drugs where id_drug=id_d) = 0 then
       raise exception 'There is no drug left!';
    else
       insert into sales(id_sale, id_drug, id_employee, amount_sale, date_time_sale, id_client) values(ind+1, id_d, id_e, count_sale, d_o_s, id_c);
       UPDATE drugs set amount = amount - count_sale where id_drug = id_d;
       end if;
END
$do$;

CALL update_amount_sale(1, 2, 10, '2022-12-11', '7316193360');

--добавление сотрудника, проверка возраста
create or replace function age_check() returns trigger as $psql$
    declare age integer;

    begin
        age = date_part('year',age(new.d_o_b::date));
        if (age < 18) then
            RAISE EXCEPTION 'Too young!';
        end if;
        return new;
    end;
$psql$ language plpgsql;

create trigger age_check before insert on employees
for each row execute procedure age_check();

insert into employees(id_position, id_address, id_phone, d_o_b, name)
values(4, 3, 3, '2000-12-16', 'Somova Alina Sergeevna');

--добавление номера телефона, проверка первого символа
create or replace function phone_check() returns trigger as $psql$
    declare num varchar(15);

    begin
        num = new.phone_number;
        if (num not like '8%') then
            RAISE EXCEPTION 'Wrong number format!';
        end if;
        return new;
    end;
$psql$ language plpgsql;

create trigger phone_check before insert on phone_numbers
for each row execute procedure phone_check();

insert into phone_numbers(id_phone_number, phone_number, description)
values((select max(id_phone_number) from phone_numbers)+1, '89966456523','work phone number')




select current_user;


