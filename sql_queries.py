# DROP TABLES

pay_table_drop = "DROP TABLE IF EXISTS pay"
pay_period_table_drop = "DROP TABLE IF EXISTS pay_period"
payroll_type_table_drop = "DROP TABLE IF EXISTS payroll_type"
office_table_drop = "DROP TABLE IF EXISTS office"
employee_table_drop = "DROP TABLE IF EXISTS employee"
legislative_entity_table_drop = "DROP TABLE IF EXISTS legislative_entity"
city_table_drop = "DROP TABLE IF EXISTS city"

# CREATE TABLES

pay_table_create = ("""
    CREATE TABLE IF NOT EXISTS pay( 
    pay_key SERIAL PRIMARY KEY, 
    pay_rate float NOT NULL,
    pay_period integer,
    pay_year integer,
    pay_period_key integer, 
    payroll_type text,
    payroll_type_key integer,
    legislative_entity text,
    employee_name text,
    employee_title text,
    employee_key integer,
    city text, 
    office_name text, 
    office_key integer
    )
""")
pay_period_table_create = ("""
    CREATE TABLE IF NOT EXISTS pay_period(
    pay_period_key SERIAL PRIMARY KEY,
    pay_period integer,
    pay_year integer,
    pay_period_begin_date timestamp, 
    pay_period_end_date timestamp, 
    check_date timestamp
    )
""")
payroll_type_table_create = ("""
    CREATE TABLE IF NOT EXISTS payroll_type( 
    payroll_type_key SERIAL PRIMARY KEY,
    payroll_type text unique
    )
""")
office_table_create = ("""
    CREATE TABLE IF NOT EXISTS office(
    office_key SERIAL PRIMARY KEY, 
    office_name text, 
    city text,
    city_key integer
    )
""")
employee_table_create = ("""
    CREATE TABLE IF NOT EXISTS employee(
    employee_key SERIAL PRIMARY KEY, 
    employee_name text, 
    employee_title text,
    legislative_entity text,
    legislative_entity_key integer
    )
""")
legislative_entity_table_create = ("""
    CREATE TABLE IF NOT EXISTS legislative_entity(
    legislative_entity_key SERIAL PRIMARY KEY, 
    legislative_entity text unique
    )
""")
city_table_create = ("""
    CREATE TABLE IF NOT EXISTS city(
    city_key SERIAL PRIMARY KEY, 
    city text unique
    )
""")

# INSERT RECORDS

pay_table_insert = ("""
    INSERT INTO pay(
    pay_rate, pay_period, pay_year, payroll_type, employee_name, city, office_name, legislative_entity, employee_title)
    VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s)
""")
pay_period_table_insert = ("""
    INSERT INTO pay_period(
    pay_period, pay_year, pay_period_begin_date, pay_period_end_date, check_date)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT DO NOTHING
""")
payroll_type_table_insert = ("""
    INSERT INTO payroll_type(payroll_type)
    VALUES (%s)
    ON CONFLICT DO NOTHING
""")
office_table_insert = ("""
    INSERT INTO office(office_name, city)
    VALUES (%s, %s)
    ON CONFLICT DO NOTHING
""")
employee_table_insert = ("""
    INSERT INTO employee (employee_name, employee_title, legislative_entity)
    VALUES (%s, %s, %s)
    ON CONFLICT DO NOTHING
""")
legislative_entity_insert = ("""
    INSERT INTO legislative_entity(legislative_entity)
    VALUES (%s)
    ON CONFLICT DO NOTHING
""")
city_table_insert = ("""
    INSERT INTO city(city)
    VALUES (%s)
    ON CONFLICT DO NOTHING
""")

# DELETE DUPLICATES
employee_table_delete = ("""
    DELETE 
    FROM 
        employee e
            USING employee e2
    WHERE
        e.employee_key < e2.employee_key
        AND e.employee_name = e2.employee_name
        AND e.employee_title = e2.employee_title
        AND e.legislative_entity = e2.legislative_entity
""")
office_table_delete = ("""
    DELETE
    FROM office o
            USING office o2
    WHERE
        o.office_key < o2.office_key
        AND o.office_name = o2.office_name
        AND o.city = o2.city
""")
# UPDATE TABLES

employee_table_update = ("""
    UPDATE employee
    SET legislative_entity_key =(
    SELECT legislative_entity_key
    FROM legislative_entity
    WHERE employee.legislative_entity = legislative_entity.legislative_entity);
""")
office_table_update = ("""
    UPDATE office
    SET city_key = (
    SELECT city_key
    FROM city
    WHERE office.city = city.city)
""")
pay_table_update = ("""
    UPDATE pay
    SET pay_period_key = (
    SELECT pay_period_key
    FROM pay_period
    WHERE pay.pay_year = pay_period.pay_year
    AND pay.pay_period = pay_period.pay_period);
    UPDATE pay
    SET payroll_type_key = (
    SELECT payroll_type_key
    FROM payroll_type
    WHERE pay.payroll_type = payroll_type.payroll_type);
    UPDATE pay
    SET employee_key = (
    SELECT employee_key
    FROM employee
    WHERE pay.employee_name = employee.employee_name
    AND pay.legislative_entity = employee.legislative_entity
    AND pay.employee_title = employee.employee_title);
    UPDATE pay
    SET office_key = (
    SELECT office_key
    FROM office
    WHERE pay.office_name = office.office_name
    AND pay.city = office.city);
""")

# DROP COLUMNS
employee_table_drop_column =("""
    ALTER TABLE employee
    DROP COLUMN "legislative_entity"
""")
office_table_drop_column = ("""
    ALTER TABLE office
    DROP COLUMN "city"
""")
pay_table_drop_column = ("""
    ALTER TABLE pay
    DROP COLUMN pay_period, 
    DROP COLUMN pay_year, 
    DROP COLUMN payroll_type, 
    DROP COLUMN legislative_entity, 
    DROP COLUMN employee_name, 
    DROP COLUMN employee_title, 
    DROP COLUMN city, 
    DROP COLUMN office_name
""")

# QUERY LISTS

create_table_queries = [
    pay_table_create, pay_period_table_create, payroll_type_table_create, office_table_create, employee_table_create, legislative_entity_table_create, city_table_create
]
drop_table_queries = [
    pay_table_drop, pay_period_table_drop, payroll_type_table_drop, office_table_drop, employee_table_drop, legislative_entity_table_drop, city_table_drop
]
delete_duplicate_rows_queries = [
    employee_table_delete, office_table_delete
]
update_columns_queries =[
    employee_table_update, office_table_update, pay_table_update
]
drop_column_queries = [
    employee_table_drop_column, office_table_drop_column, pay_table_drop_column
]

