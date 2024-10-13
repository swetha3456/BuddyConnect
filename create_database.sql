CREATE TABLE users (
    email VARCHAR(100) UNIQUE NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    gender CHAR(1) NOT NULL,
    password VARCHAR(100) NOT NULL
);

CREATE TABLE events (
    event_id INT AUTO_INCREMENT PRIMARY KEY,
    event_name VARCHAR(100) NOT NULL,
    event_type VARCHAR(50) NOT NULL,
    venue VARCHAR(100) NOT NULL,
    event_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    created_by VARCHAR(100) NOT NULL,
    FOREIGN KEY (created_by) REFERENCES users(email) ON DELETE CASCADE
);

CREATE TABLE user_interests (
    email VARCHAR(100) NOT NULL,
    interest VARCHAR(100) NOT NULL,
    PRIMARY KEY (email, interest),
    FOREIGN KEY (email) REFERENCES users(email) ON DELETE CASCADE
);

CREATE TABLE requests (
    event_id INT NOT NULL,
    user_email INT NOT NULL,
    status VARCHAR(100) NOT NULL DEFAULT("PENDING"),
    FOREIGN KEY (user_email) REFERENCES users(email) ON DELETE CASCADE,
    FOREIGN KEY (event_id) REFERENCES events(event_id) ON DELETE CASCADE
);