-- Switch to the desired database
CREATE DATABASE medimap;

\c medimap;

-- Create the HOSPITAL table
CREATE TABLE HOSPITAL(
    id SERIAL PRIMARY KEY,
    hospital_name VARCHAR(32) NOT NULL,
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    addr VARCHAR(128) NOT NULL,
    city VARCHAR(32) NOT NULL,
    state_name VARCHAR(32) NOT NULL,
    pincode INT NOT NULL,
    contact VARCHAR(12)
);

--Consists of relation (M:N) mapping
CREATE TABLE CONSISTS_OF(
    hid INT,
    rid INT,
    available BOOLEAN DEFAULT FALSE,
    total_quantiy INT DEFAULT 0,
    total_available_quantity INT default 0,
    FOREIGN KEY (hid) REFERENCES HOSPITAL(id) ON DELETE CASCADE,
    FOREIGN KEY (rid) REFERENCES RESOURCES(id) ON DELETE CASCADE
)

-- Create the RESOURCES table
CREATE TABLE RESOURCES(
    id SERIAL PRIMARY KEY,
    dept VARCHAR(64),
    resource_type VARCHAR(64) 
);

-- Create the INSURANCE table
CREATE TABLE INSURANCE(
    id SERIAL PRIMARY KEY,
    company_name VARCHAR(32) UNIQUE,
    cover INT NOT NULL,
    addr VARCHAR(255),
    email VARCHAR(225),
    website_url VARCHAR(225)
);

-- Create the PATIENT table
CREATE TABLE PATIENT (
    id SERIAL PRIMARY KEY,
    hid INT,
    insurance_id INT,
    accident_id INT,
    pname VARCHAR(64),
    gender VARCHAR(16),
    bloodgroup VARCHAR(2),
    contact VARCHAR(12),
    FOREIGN KEY (hid) REFERENCES hospital(id) ON DELETE CASCADE,
    FOREIGN KEY (insurance_id) REFERENCES INSURANCE(id) ON DELETE SET NULL,
    FOREIGN KEY (accident_id) REFERENCES ACCIDENT(id)
    ON DELETE CASCADE
);

CREATE TABLE ALLOCATED(
    rid INT,
    patient_id INT,
    quatity_allocated INT,
    FOREIGN KEY(rid) REFERENCES RESOURCES(id) ,
    FOREIGN KEY(patient_id) REFERENCES PATIENT(id) 
)



-- Create the ACCIDENT table
CREATE TABLE ACCIDENT(
    id SERIAL PRIMARY KEY,
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    accident_details JSONB 
);





\c postgres 