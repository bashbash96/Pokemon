drop database pokemons_db;
create database pokemons_db;

use pokemons_db;

CREATE TABLE trainer(
    name varchar(20) NOT NULL PRIMARY KEY,
    town VARCHAR(50)
);

CREATE TABLE pokemon(
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(20),
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

CREATE TABLE type(
    type_name varchar(30) NOT NULL PRIMARY KEY
);

CREATE TABLE types_pokemon(

    type_name varchar(30) ,
    pokemon_id int,

    foreign key(pokemon_id) references pokemon(id),
    foreign key(type_name) references type(type_name),
    PRIMARY KEY (type_name, pokemon_id)
);