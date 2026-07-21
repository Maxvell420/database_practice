DROP TABLE IF EXISTS messengers_requests;
DROP TABLE IF EXISTS users_states;
DROP TABLE IF EXISTS nasapower_geohashes_data;
DROP TABLE IF EXISTS geohashes;

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

-- в этих таблицах надо будет уйти от id на uuid
CREATE TABLE IF NOT EXISTS messengers_requests(
    id SERIAL PRIMARY KEY,
    messenger_type INT NOT NULL,
    data JSON NOT NULL,
    request_uuid VARCHAR(50) NOT NULL,
    user_uid VARCHAR(36) DEFAULT NULL,
    processed_at TIMESTAMP DEFAULT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS users_states(
    id SERIAL PRIMARY KEY,
    messenger_type INT NOT NULL,
    user_uid VARCHAR(36) NOT NULL,
    state int NOT NULL,
    data JSON NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    unique(messenger_type, user_uid)
);