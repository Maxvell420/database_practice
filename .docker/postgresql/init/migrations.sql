create table if not exists users (
    id serial primary key,
    name varchar(255) not null,
    email varchar(255) not null,
    password varchar(255) not null
);

create table if not exists map_power_polygons(
    id SERIAL PRIMARY KEY,
    polygon geometry(POLYGON, 4326)  -- 4326 = WGS84 (широта/долгота)
);

create table if not exists nasapower_polygons_data(
    id SERIAL PRIMARY KEY,
    polygon_id INT NOT NULL,
    data_type VARCHAR(25) NOT NULL,
    date_from INT NOT NULL,
    date_to INT NOT NULL,
    data JSON NOT NULL,
    FOREIGN KEY (polygon_id) REFERENCES map_power_polygons(id)
);