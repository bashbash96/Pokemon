import pymysql
import json
from config import DB_PASSWORD

connection = pymysql.connect(
    host='localhost',
    user='root',
    password=DB_PASSWORD,
    db='sql_in_python',
    charset='utf8',
    cursorclass=pymysql.cursors.DictCursor
)


def add_pokemon_to_db(cursor, pokemon, table_name):
    temp_pokemon = pokemon.copy()
    del temp_pokemon['ownedBy']
    try:
        columns = ', '.join("`" + str(x).replace('/', '_') + "`" for x in temp_pokemon.keys())
        values = ', '.join("'" + str(x).replace('/', '_') + "'" for x in temp_pokemon.values())
        query = "INSERT into %s (%s) VALUES (%s);" % (table_name, columns, values)
        cursor.execute(query)
        connection.commit()
    except Exception as e:
        print("Error while adding pokemon", e)


def add_trainer_to_db(cursor, trainer, table_name):
    try:
        columns = ', '.join("`" + str(x).replace('/', '_') + "`" for x in trainer.keys())
        values = ', '.join("'" + str(x).replace('/', '_') + "'" for x in trainer.values())
        query = "INSERT into %s (%s) VALUES (%s);" % (table_name, columns, values)
        cursor.execute(query)
        connection.commit()
    except Exception as e:
        print("Error while adding trainer to db", e)


def connect_pokemon_to_trainer(cursor, trainer_name, pokemon_id, table_name):
    try:
        columns = ', '.join("`" + str(x).replace('/', '_') + "`" for x in ['trainer_name', 'pokemon_id'])
        values = ', '.join("'" + str(x).replace('/', '_') + "'" for x in [trainer_name, pokemon_id])
        query = "INSERT into %s (%s) VALUES (%s);" % (table_name, columns, values)
        cursor.execute(query)
        connection.commit()
    except Exception as e:
        print("Error while connecting pokemon to trainer", e)


def main():
    try:
        with connection.cursor() as cursor:
            with open('data.json', 'r') as fid:
                data = json.load(fid)
                for pokemon in data:
                    add_pokemon_to_db(cursor, pokemon, 'pokemon')
                    for trainer in pokemon.get('ownedBy'):
                        add_trainer_to_db(cursor, trainer, 'trainer')
                        connect_pokemon_to_trainer(cursor, trainer.get('name'), pokemon.get('id'), 'trainer_pokemon')
    except Exception as err:
        print("500 - Internal error", err)


main()
