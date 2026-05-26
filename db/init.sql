DROP TABLE IF EXISTS user_profiles;

CREATE TABLE user_profiles (

    user_id INTEGER PRIMARY KEY,

    age INTEGER,

    gender VARCHAR(20),

    department VARCHAR(100),

    job_role VARCHAR(100),

    marital_status VARCHAR(50),

    monthly_income INTEGER
);