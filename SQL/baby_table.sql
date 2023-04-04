CREATE TABLE baby_table (
    baby_id SERIAL PRIMARY KEY,
    mother_name VARCHAR(30),
    baby_name VARCHAR(30),
    baby_surname VARCHAR(30),
    baby_gender CHAR(1), -- M (male) or F (female)
    birth_date DATE,
    birth_hour TIME,
    gestation_week SMALLINT,
    gestation_week_plus_day SMALLINT,
    birth_weight FLOAT,
    birth_type BOOLEAN 
);