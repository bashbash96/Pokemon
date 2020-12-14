from flask import Flask, Response, request
import json
from database import main_db

app = Flask(__name__)


@app.route("/pokemon/")
def pokemon_filter():
    args = dict(request.args)
    if 'type' in args:
        response = {'pokemons': main_db('get_pokemons_by_type', args['type'])}
    elif 'trainer' in args:
        response = {'pokemons': main_db('get_pokemons_by_trainer', args['trainer'])}
    else:
        response = {'error': 'Invalid filter', 'detail': 'Invalid pokemon filter'}
        return Response(json.dumps(response)), 400

    return Response(json.dumps(response)), 200


# ex5
@app.route("/trainer/")
def trainer_filter():
    args = dict(request.args)
    if 'pokemon' in args:
        response = {'trainers': main_db('get_trainers_of_pokemon', args['pokemon'])}
    else:
        response = {'error': 'Invalid filter', 'detail': 'Invalid trainer filter'}
        return Response(json.dumps(response)), 400

    return Response(json.dumps(response)), 200


port_number = 3000
if __name__ == '__main__':
    app.run(port=port_number)
