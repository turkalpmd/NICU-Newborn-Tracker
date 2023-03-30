CREATE TABLE doctors(
doctor_id SMALLSERIAL PRIMARY KEY,
doctor_name VARCHAR(30),
doctor_surname VARCHAR(30),
doctor_email VARCHAR(50),
doctor_phone_number VARCHAR(13),
doctor_organization_id SMALLINT
)