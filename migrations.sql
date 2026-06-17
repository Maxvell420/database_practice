CREATE TABLE IF NOT EXISTS geohashes(
    id SERIAL PRIMARY KEY,
    geohash char(5) not null
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