/* Создать модифицируемое представление для таблицы с самым
большим числом полей. В представлении скрыть хотя бы один столбец и
несколько строк. Выполнить для полученного представления запрос INSERT.
*/

CREATE VIEW c_v AS
    SELECT car_vin, color, id_driver FROM cars WHERE color != 'white';
INSERT INTO c_v (car_vin, color, id_driver) VALUES ('111111111119', 'yellow', '1933607316');


SELECT * FROM c_v;

/* Создать представление по нарушениям с указанием вида нарушения и размером штрафа */
CREATE VIEW violations_view AS
SELECT id, violation_description, max_sanction FROM violations, violation_types
WHERE violation_type_id = violation_type;


SELECT * FROM violations_view;

 /*
Создать представление по водителям с указанием количества нарушений, количества различных типов
нарушений и суммы штрафов
 */
CREATE VIEW drivers_view AS
SELECT name, COUNT(violation_id) as c1, COUNT(DISTINCT violation_type_id) as c2 FROM drivers
LEFT JOIN violation_per_driver vpd ON drivers.id = vpd.driver_id
LEFT JOIN violations v ON vpd.violation_id = v.id
LEFT JOIN violation_types vt ON v.violation_type_id = vt.violation_type
GROUP BY name;


SELECT * FROM drivers_view;
