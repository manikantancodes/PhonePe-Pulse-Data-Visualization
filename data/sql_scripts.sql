-- Create the necessary tables for the project

CREATE TABLE aggregated_insurance (
    States VARCHAR(50),
    Years INT,
    Quarter INT,
    Transaction_type VARCHAR(50),
    Transaction_count BIGINT,
    Transaction_amount BIGINT
);

CREATE TABLE aggregated_transaction (
    States VARCHAR(50),
    Years INT,
    Quarter INT,
    Transaction_type VARCHAR(50),
    Transaction_count BIGINT,
    Transaction_amount BIGINT
);

CREATE TABLE aggregated_user (
    States VARCHAR(50),
    Years INT,
    Quarter INT,
    Brands VARCHAR(50),
    Transaction_count BIGINT,
    Percentage FLOAT
);

CREATE TABLE map_insurance (
    States VARCHAR(50),
    Years INT,
    Quarter INT,
    Districts VARCHAR(50),
    Transaction_count BIGINT,
    Transaction_amount BIGINT
);

CREATE TABLE map_transaction (
    States VARCHAR(50),
    Years INT,
    Quarter INT,
    District VARCHAR(50),
    Transaction_count BIGINT,
    Transaction_amount BIGINT
);

CREATE TABLE map_user (
    States VARCHAR(50),
    Years INT,
    Quarter INT,
    District VARCHAR(50),
    RegisteredUsers BIGINT,
    AppOpens BIGINT
);

CREATE TABLE top_insurance (
    States VARCHAR(50),
    Years INT,
    Quarter INT,
    Pincodes VARCHAR(50),
    Transaction_count BIGINT,
    Transaction_amount BIGINT
);

CREATE TABLE top_transaction (
    States VARCHAR(50),
    Years INT,
    Quarter INT,
    Pincodes VARCHAR(50),
    Transaction_count BIGINT,
    Transaction_amount BIGINT
);

CREATE TABLE top_user (
    States VARCHAR(50),
    Years INT,
    Quarter INT,
    Pincodes VARCHAR(50),
    RegisteredUsers BIGINT
);


This SQL script creates the following tables:

aggregated_insurance
aggregated_transaction
aggregated_user
map_insurance
map_transaction
map_user
top_insurance
top_transaction
top_user

Each table has columns for States, Years, Quarter, and other relevant columns based on the data they store, such as Transaction_type, Transaction_count, Transaction_amount, Brands, Districts, Pincodes, RegisteredUsers, and AppOpens.
You can add additional constraints like primary keys, foreign keys, and indexes as per your requirements by modifying this script.
Note: Make sure to execute this script in your PostgreSQL database to create the necessary tables before running your Python code.