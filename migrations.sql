CREATE TABLE IF NOT EXISTS geohashes(
    id SERIAL PRIMARY KEY,
    geohash char(5) not null unique
);

CREATE TABLE IF NOT EXISTS nasapower_geohashes_data(
    id SERIAL PRIMARY KEY,
    geohash_id INT NOT NULL,
    data_type VARCHAR(25) NOT NULL,
    timestamp_from INT NOT NULL,
    timestamp_to INT NOT NULL,
    data JSON NOT NULL,
    FOREIGN KEY (geohash_id) REFERENCES geohashes(id)
);

CREATE TABLE IF NOT EXISTS messengers_requests(
    id SERIAL PRIMARY KEY,
    messenger_type INT NOT NULL,
    data JSON NOT NULL,
    request_uuid VARCHAR(50) NOT NULL,
    user_uuid VARCHAR(36) DEFAULT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS messengers_responses(
    id SERIAL PRIMARY KEY,
    messenger_type INT NOT NULL,
    request_id INT NOT NULL,
    response_uuid VARCHAR(36) DEFAULT NULL,
    data JSON NOT NULL,
    user_uuid VARCHAR(36) DEFAULT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS users_states(
    messenger_type INT NOT NULL,
    user_uuid VARCHAR(36) NOT NULL,
    state int NOT NULL,
    data JSON NOT NULL
);