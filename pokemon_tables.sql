-- drop database sql_in_python
-- create database sql_in_python;

use sql_in_python;

CREATE TABLE trainer(
    name varchar(20) NOT NULL PRIMARY KEY,
    town VARCHAR(50)
);

CREATE TABLE pokemon(
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(20),
    type VARCHAR(30),
    height int,
    weight int
);


CREATE TABLE trainer_pokemon(
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    trainer_name varchar(20),
    pokemon_id int,

    foreign key(trainer_name) references trainer(name),
    foreign key(pokemon_id) references pokemon(id)
);
