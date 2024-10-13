CREATE TABLE users (
    email VARCHAR(100) UNIQUE NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    gender CHAR(1) NOT NULL,
    location VARCHAR(100) NOT NULL,
    password VARCHAR(100) NOT NULL
);

CREATE TABLE events (
    event_id INTEGER PRIMARY KEY AUTOINCREMENT, 
    event_name VARCHAR(100) NOT NULL,
    event_type VARCHAR(50) NOT NULL,
    venue VARCHAR(100) NOT NULL,
    location VARCHAR(100) NOT NULL,
    event_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    description VARCHAR(600),
    created_by VARCHAR(100) NOT NULL,
    FOREIGN KEY (created_by) REFERENCES users(email) ON DELETE CASCADE
);

CREATE TABLE user_interests (
    email VARCHAR(100) NOT NULL,
    interest VARCHAR(100) NOT NULL,
    PRIMARY KEY (email, interest),
    FOREIGN KEY (email) REFERENCES users(email) ON DELETE CASCADE
);