CREATE TABLE babies(
baby_id VARCHAR(32) PRIMARY KEY,
baby_mother_name VARCHAR(30),
baby_surname VARCHAR(30),
baby_name VARCHAR(30),
baby_gender SMALLINT,
baby_date_of_birth TIMESTAMP,
baby_birth_week SMALLINT,
baby_birth_day_of_week varchar(15),
baby_birth_weight FLOAT,
baby_birth_type VARCHAR(10),
couveuse_id INT,
doctor_id INT,   
FOREIGN KEY(doctor_id) 
    REFERENCES doctors(doctor_id)    
)