-- Switch to the desired database
CREATE DATABASE medimap;

\c medimap;

-- Create the HOSPITAL table
CREATE TABLE HOSPITAL(
    id SERIAL PRIMARY KEY,
    hospital_name VARCHAR(32) NOT NULL,
    addr VARCHAR(128) NOT NULL,
    city VARCHAR(32) NOT NULL,
    state_name VARCHAR(32) NOT NULL,
    pincode INT NOT NULL,
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    contact VARCHAR(12)
);

-- Create the RESOURCES table
CREATE TABLE RESOURCES(
    id SERIAL PRIMARY KEY,
    hospital_id INT,
    dept VARCHAR(32) NOT NULL,
    resource_type VARCHAR(32),
    quantity INT,
    occupied_quantity INT DEFAULT 0,
    FOREIGN KEY (hospital_id) REFERENCES HOSPITAL(id)
        ON DELETE CASCADE
);

-- Create the INSURANCE table
CREATE TABLE INSURANCE(
    id SERIAL PRIMARY KEY,
    provider_name VARCHAR(32) UNIQUE,
    cover INT NOT NULL
);

-- Create the PATIENT table
CREATE TABLE PATIENT (
    id SERIAL PRIMARY KEY,
    name VARCHAR(64) NOT NULL,
    gender VARCHAR(16) NOT NULL,
    contact VARCHAR(12),
    hospital_id INT,
    FOREIGN KEY (hospital_id) REFERENCES HOSPITAL(id)
        ON DELETE SET NULL,
    insurance_id INT,
    FOREIGN KEY (insurance_id) REFERENCES INSURANCE(id)
        ON DELETE CASCADE
);



-- Create the ACCIDENT table
CREATE TABLE ACCIDENT(
    id SERIAL PRIMARY KEY,
    patient_id INT NOT NULL,
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    accident_details JSONB ,
    FOREIGN KEY (patient_id) REFERENCES PATIENT(id)
        ON DELETE CASCADE
);





\c postgres 