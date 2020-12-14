import json
from database import main_db


with open("poke_data.json", 'r+') as data:
    data = json.load(data)
    for poke in data:
        poke['types'] = [poke['type']]
        main_db('add_pokemon', poke)
        for trainer in poke.get('ownedBy'):
            main_db('add_trainer', trainer)
            main_db('connect_pokemon_to_trainer', trainer.get('name'), poke.get('id'))
