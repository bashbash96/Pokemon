import json
from database import main_db


with open("data.json", 'r+') as data:
    data = json.load(data)
    for poke in data:
        poke['types'] = [poke['type']]
        main_db('add_pokemon', poke)
