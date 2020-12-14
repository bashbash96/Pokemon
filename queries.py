import pymysql
from config import DB_PASSWORD
connection = pymysql.connect(
    host='localhost',
    user='root',
    password=DB_PASSWORD,
    db='sql_in_python',
    charset='utf8',
    cursorclass=pymysql.cursors.DictCursor
)


def ex1():
    try:
        with connection.cursor() as cursor:
            query = 'select * from pokemon where weight = (select max(weight) from pokemon)'
            cursor.execute(query)
            res = cursor.fetchall()
            return res[0]
    except Exception as err:
        print("500 - Internal error", err)


# print(ex1())

def ex2(type_):
    try:
        with connection.cursor() as cursor:
            query = f'select name from pokemon where type = "{type_}"'
            cursor.execute(query)
            res = [val.get('name') for val in cursor.fetchall()]
            return res
    except Exception as err:
        print("500 - Internal error", err)


# print(ex2('grass'))

def ex3(pokemon_name):
    try:
        with connection.cursor() as cursor:
            pokemon_name = "\"" + str(pokemon_name).replace('/', '_') + "\""
            query = 'select t.name from pokemon as p join trainer as t join trainer_pokemon as tp ' \
                    'on p.id = tp.pokemon_id and t.name = tp.trainer_name ' \
                    'where p.name = ' + pokemon_name
            cursor.execute(query)
            res = [val.get('name') for val in cursor.fetchall()]
            return res
    except Exception as err:
        print("500 - Internal error", err)


# print(ex3('gengar'))

def ex4(trainer_name):
    try:
        with connection.cursor() as cursor:
            trainer_name = "\"" + str(trainer_name).replace('/', '_') + "\""
            query = 'select p.name from pokemon as p join trainer as t join trainer_pokemon as tp ' \
                    'on p.id = tp.pokemon_id and t.name = tp.trainer_name ' \
                    'where t.name = ' + trainer_name
            cursor.execute(query)
            res = [val.get('name') for val in cursor.fetchall()]
            return res
    except Exception as err:
        print("500 - Internal error", err)


# print(ex4('Loga'))

def extension():
    try:
        with connection.cursor() as cursor:
            query = 'select max(trainer_count) as max_count from ' \
                    '(select count(*) as trainer_count from trainer_pokemon group by pokemon_id) as t'

            cursor.execute(query)
            res = cursor.fetchall()
            max_count = res[0].get('max_count')

            query = 'select * from pokemon ' \
                    'where id in ' \
                    '(select pokemon_id from trainer_pokemon group by pokemon_id having ' \
                    'count(*) = ' + str(max_count) + ')'
            cursor.execute(query)
            res = cursor.fetchall()
            return res
    except Exception as err:
        print("500 - Internal error", err)

# print(extension())
