CREATE TABLE babies(
baby_id VARCHAR(32) PRIMARY KEY,
mother_name VARCHAR(30),
baby_surname VARCHAR(30),
baby_name VARCHAR(30),
baby_gender CHAR,
birth_date DATE,
gestation_week SMALLINT,
gestation_week_plus_day SMALLINT,
birth_weight FLOAT,
birth_type BOOLEAN,
birth_hour SMALLINT,
doctor_id INT,   
FOREIGN KEY(doctor_id) 
    REFERENCES doctors(doctor_id)    
)