CREATE DATABASE medimap;

\c medimap ;

CREATE TABLE HOSPITAL(
    id  SERIAL PRIMARY KEY,
    hospital_name VARCHAR(32) NOT NULL,
    addr VARCHAR(128) NOT NULL,
    city VARCHAR(32) NOT NULL,
    state_name VARCHAR(32) NOT NULL,
    pincode INT NOT NULL,
    latitude DOUBLE PRECISION NOT NULL,
    longitude  DOUBLE PRECISION NOT NULL,
    contact VARCHAR(12)
);



CREATE TABLE RESOURCES(
    id SERIAL PRIMARY KEY,
    hospital_id INT ,
    dept VARCHAR(32) NOT NULL,
    resource_type VARCHAR(32),
    quantity INT,
    occupied_quantity  INT,
    FOREIGN KEY (hospital_id) REFERENCES HOSPITAL(id)
        ON DELETE CASCADE
);

\c postgres