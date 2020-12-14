import pymysql
from config import DB_PASSWORD, DB_NAME
import requests
from evolve import evolve

connection = pymysql.connect(
    host='localhost',
    user='root',
    password=DB_PASSWORD,
    db=DB_NAME,
    charset='utf8',
    cursorclass=pymysql.cursors.DictCursor
)


def add_pokemon(cursor, args, table_name):
    pokemon = args[0]
    temp_pokemon = {}
    attributes = {'id', 'name', 'ownedBy', 'types', 'height', 'weight'}
    for attribute in attributes:
        temp_pokemon[attribute] = pokemon.get(attribute, None)

    trainers = temp_pokemon['ownedBy']
    del temp_pokemon['ownedBy']
    types = temp_pokemon['types']
    del temp_pokemon['types']
    try:
        columns = ', '.join("`" + str(x).replace('/', '_') + "`" for x in temp_pokemon.keys())
        values = ', '.join("'" + str(x).replace('/', '_') + "'" for x in temp_pokemon.values())
        query = "INSERT into %s (%s) VALUES (%s);" % (table_name, columns, values)
        cursor.execute(query)
        connection.commit()
        _id = temp_pokemon['id']
        if types:
            add_types_of_pokemon(cursor, _id, types)
        if trainers:
            for trainer in trainers:
                main_db('add_trainer', trainer)
                main_db('connect_pokemon_to_trainer', trainer.get('name'), temp_pokemon['id'])
    except Exception as e:
        return {'error': 500, 'details': 'adding pokemon ' + str(e)}


def add_trainer(cursor, args, table_name):
    trainer = args[0]
    try:
        columns = ', '.join("`" + str(x).replace('/', '_') + "`" for x in trainer.keys())
        values = ', '.join("'" + str(x).replace('/', '_') + "'" for x in trainer.values())
        query = "INSERT into %s (%s) VALUES (%s);" % (table_name, columns, values)
        cursor.execute(query)
        connection.commit()
    except Exception as e:
        return {'error': 500, 'details': 'adding trainer ' + str(e)}


def connect_pokemon_to_trainer(cursor, args, table_name):
    trainer_name, pokemon_id = args[0], args[1]
    try:
        columns = ', '.join("`" + str(x).replace('/', '_') + "`" for x in ['trainer_name', 'pokemon_id'])
        values = ', '.join("'" + str(x).replace('/', '_') + "'" for x in [trainer_name, pokemon_id])
        query = "INSERT into %s (%s) VALUES (%s);" % (table_name, columns, values)
        cursor.execute(query)
        connection.commit()
    except Exception as e:
        return {'error': 500, 'details': 'connecting pokemon to trainer ' + str(e)}


def get_pokemons_by_type(cursor, args):
    pok_type = args[0]
    try:
        query = f"select name from pokemon where type = '{pok_type}'"
        cursor.execute(query)
        res = [val.get('name') for val in cursor.fetchall()]
        return res
    except Exception as e:
        return {'error': 500, 'details': 'get pokemons by type ' + str(e)}


def get_pokemons_by_trainer(cursor, args):
    trainer_name = args[0]
    try:
        trainer_name = "\"" + str(trainer_name).replace('/', '_') + "\""
        query = 'select p.name from pokemon as p join trainer_pokemon as tp ' \
                'on p.id = tp.pokemon_id ' \
                'where tp.trainer_name = ' + trainer_name
        cursor.execute(query)
        res = cursor.fetchall()
        res = [val.get('name') for val in res]
        return res
    except Exception as e:
        return {'error': 500, 'details': 'get pokemons by trainer ' + str(e)}


def get_trainers_of_pokemon(cursor, args):
    pokemon_name = args[0]
    try:
        pokemon_name = "\"" + str(pokemon_name).replace('/', '_') + "\""
        query = 'select tp.trainer_name as name from pokemon as p join trainer_pokemon as tp ' \
                'on p.id = tp.pokemon_id ' \
                'where p.name = ' + pokemon_name
        cursor.execute(query)
        res = cursor.fetchall()
        res = [val.get('name') for val in res]
        return res
    except Exception as e:
        return {'error': 500, 'details': 'get trainers of pokemon ' + str(e)}


def delete_pokemon_of_trainer(cursor, args):
    trainer_name = args[0]
    pokemon_name = args[1]
    try:
        pokemon_name = "\"" + str(pokemon_name).replace('/', '_') + "\""
        trainer_name = "\"" + str(trainer_name).replace('/', '_') + "\""
        query = 'select p.id from pokemon as p where p.name = ' + pokemon_name
        cursor.execute(query)
        res = cursor.fetchall()
        if len(res) == 0:
            raise
        pokemon_id = res[0].get('id')
        query = "delete from trainer_pokemon as tp where tp.trainer_name = %s and tp.pokemon_id = %s" % (
            trainer_name, pokemon_id)
        cursor.execute(query)
        connection.commit()
    except Exception as e:
        return {'error': 500, 'details': 'deleting pokemon from trainer ' + str(e)}


def add_type(cursor, args, table_name):
    type_name = args[0]
    try:
        columns = ', '.join("`" + str(x).replace('/', '_') + "`" for x in ['type_name'])
        values = ', '.join("'" + str(x).replace('/', '_') + "'" for x in [type_name])
        query = "INSERT into %s (%s) VALUES (%s);" % (table_name, columns, values)
        cursor.execute(query)
        connection.commit()
    except Exception as e:
        return {'error': 500, 'details': 'Adding type ' + str(e)}


def connect_type_to_pokemon(cursor, args, table_name):
    type_name, pokemon_id = args[0], args[1]
    try:
        columns = ', '.join("`" + str(x).replace('/', '_') + "`" for x in ['type_name', 'pokemon_id'])
        values = ', '.join("'" + str(x).replace('/', '_') + "'" for x in [type_name, pokemon_id])
        query = "INSERT into %s (%s) VALUES (%s);" % (table_name, columns, values)
        cursor.execute(query)
        connection.commit()
    except Exception as e:
        return {'error': 500, 'details': 'connecting pokemon to type ' + str(e)}


def get_pokemon_details(pokemon_name):
    api_url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}'
    response = requests.get(api_url)
    return response.json()


def get_types_of_pokemon(pokemon_name):
    pokemon_details = get_pokemon_details(pokemon_name)
    return [val['type']['name'] for val in pokemon_details['types']]


def get_id_by_name(cursor, pokemon_name):
    query = f"select id from pokemon where name = '{pokemon_name}'"
    cursor.execute(query)
    res = cursor.fetchall()
    return res[0]['id']


def add_types_of_pokemon(cursor, *args):
    pokemon_id = args[0]
    types_list = args[1]
    for type in types_list:
        add_type(cursor, (type,), 'type')
        connect_type_to_pokemon(cursor, (type, pokemon_id), 'types_pokemon')


def update_types(cursor, args):
    pokemon_name = args[0]
    new_types = get_types_of_pokemon(pokemon_name)
    _id = get_id_by_name(cursor, pokemon_name)
    add_types_of_pokemon(cursor, _id, new_types)


def evolve_pokemon(cursor, args):
    pokemon_name = args[0]
    try:
        evolved_pokemon = evolve(pokemon_name)
    except Exception as e:
        return {'error': 400, 'details': 'This pokemon can not be evolved ' + str(e)}
    evolved_details = get_pokemon_details(evolved_pokemon)
    update_pokemon_details(cursor, pokemon_name, evolved_details)
    update_types(cursor, (evolved_pokemon,))


def update_pokemon_details(cursor, *args):
    current_pokemon_name = args[0]
    new_pokemon_details = args[1]
    sql = f"UPDATE pokemon SET height = '{new_pokemon_details['height']}', weight = '{new_pokemon_details['weight']}' WHERE name='{current_pokemon_name}' "
    cursor.execute(sql)
    query = f"UPDATE pokemon SET name = '{new_pokemon_details['name']}' WHERE name = '{current_pokemon_name}'"
    cursor.execute(query)
    connection.commit()


def donate_pokemon(cursor, args):
    try:
        trainer_donate = args[0]
        to_trainer_name = args[1]
        pokemon_name = args[2]
        query = f"select id from pokemon where name = '{pokemon_name}'"
        cursor.execute(query)
        res = cursor.fetchall()
        _id = res[0]['id']
        query = f"UPDATE trainer_pokemon SET trainer_name = '{to_trainer_name}' WHERE trainer_name = '{trainer_donate}' AND pokemon_id = '{_id}'"
        cursor.execute(query)
        connection.commit()
    except Exception as e:
        return {'error': 500, 'details': 'donating pokemon failed ' + str(e)}


def main_db(action, *args):
    try:
        with connection.cursor() as cursor:
            if action == 'add_pokemon':
                return add_pokemon(cursor, args, 'pokemon')
            elif action == 'add_trainer':
                return add_trainer(cursor, args, 'trainer')
            elif action == 'connect_pokemon_to_trainer':
                return connect_pokemon_to_trainer(cursor, args, 'trainer_pokemon')
            elif action == 'get_pokemons_by_type':
                return get_pokemons_by_type(cursor, args)
            elif action == 'get_pokemons_by_trainer':
                return get_pokemons_by_trainer(cursor, args)
            elif action == 'get_trainers_of_pokemon':
                return get_trainers_of_pokemon(cursor, args)
            elif action == 'delete_pokemon_of_trainer':
                return delete_pokemon_of_trainer(cursor, args)
            elif action == 'update_types':
                return update_types(cursor, args)
            elif action == 'evolve_pokemon':
                return evolve_pokemon(cursor, args)
            elif action == 'donate_pokemon':
                return donate_pokemon(cursor, args)
            else:
                return {'error': 400, 'details': 'Invalid option '}
    except Exception as err:
        print("500 - Internal error", err)


if __name__ == '__main__':
    # print(main_db('get_pokemons_by_type', 'grass'))
    # print(main_db('evolve_pokemon', 'charmander'))
    # print(main_db('get_pokemons_by_trainer', 'Loga'))
    # print(main_db('update_types', 'gengar'))
    print(main_db('donate_pokemon', 'Ash', 'Candice', 'bulbasaur'))

    # print(main_db('delete_pokemon_of_trainer', 'Loga', 'metapod'))
