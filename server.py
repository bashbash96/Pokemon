from flask import Flask, Response, request
import json
from database import main_db

app = Flask(__name__)


@app.route('/pokemon/<name>', methods=['PUT'])
def pokemon_update_types(name):
    response = main_db('update_types', name)
    if response and 'error' in response:
        return Response(json.dumps(response['details'])), response['error']
    return Response(json.dumps({'Response': 'Updated successfully'})), 200


@app.route('/pokemon/evolve/<name>', methods=['PUT'])
def pokemon_evolve(name):
    response = main_db('evolve_pokemon', name)
    if response and 'error' in response:
        return Response(json.dumps(response['details'])), response['error']
    return Response(json.dumps({'Response': 'Evolved successfully'})), 200


@app.route('/pokemon/', methods=['DELETE'])
def pokemon_delete():
    args = dict(request.args)
    response = {}
    if 'pokemon' in args and 'trainer' in args:
        response = main_db('delete_pokemon_of_trainer', args['trainer'], args['pokemon'])
    if response and 'error' in response:
        return Response(json.dumps(response['details'])), response['error']
    return Response(json.dumps({'Response': 'Deleted successfully'})), 200


@app.route('/pokemon/', methods=['POST'])
def add_pokemon():
    req = request.get_json()
    attributes = ['id', 'name', 'ownedBy', 'types', 'height', 'weight']
    print(req.keys())
    if list(req.keys()) == attributes:
        response = main_db('add_pokemon', req)
    else:
        response = {'error': 400, 'details': 'Invalid pokemon object'}

    if response and 'error' in response:
        return Response(json.dumps(response['details'])), response['error']
    return Response(json.dumps({'Response': 'Added successfully'})), 200


@app.route("/pokemon/")
def pokemon_filter():
    args = dict(request.args)
    response = {}

    if 'type' in args:
        response = main_db('get_pokemons_by_type', args['type'])
        if 'error' not in response:
            response = {'pokemons': response}
    elif 'trainer' in args:
        response = main_db('get_pokemons_by_trainer', args['trainer'])
        if 'error' not in response:
            response = {'pokemons': response}
    else:
        response = {'error': 400, 'details': 'Invalid pokemon filter'}

    if response and 'error' in response:
        return Response(json.dumps(response['details'])), response['error']
    return Response(json.dumps(response)), 200


@app.route("/trainer/")
def trainer_filter():
    args = dict(request.args)
    response = {}
    if 'pokemon' in args:
        response = main_db('get_trainers_of_pokemon', args['pokemon'])
        if 'error' not in response:
            response = {'trainers': response}
    else:
        response = {'error': 400, 'detail': 'Invalid trainer filter'}

    if response and 'error' in response:
        return Response(json.dumps(response['details'])), response['error']
    return Response(json.dumps(response)), 200


@app.route("/pokemon/donate/", methods=['PUT'])
def donate_pokemon():
    args = dict(request.args)
    response = {}
    if 'donator' in args and 'receiver' in args and 'pokemon' in args:
        response = main_db('donate_pokemon', args['donator'], args['receiver'], args['pokemon'])
    if response and 'error' in response:
        return Response(json.dumps(response['details'])), response['error']
    return Response(json.dumps({'Response': 'Donated successfully'})), 200


port_number = 3000
if __name__ == '__main__':
    app.run(port=port_number)
