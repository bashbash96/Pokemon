import requests
import json


# gets pokemon name and returns specie chain dictionary
def get_evolution_chain(pokemon):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon}"
    species = requests.get(url).json()
    species_url = species.get("species").get("url")
    evolution_chain = requests.get(species_url).json()
    evolution_chain_url = evolution_chain.get("evolution_chain").get("url")
    chain = requests.get(evolution_chain_url).json().get("chain")
    return chain


def evolve_to(pokemon, evolution_chain):
    curr_specie = evolution_chain.get("species").get("name")
    if evolution_chain.get("evolves_to"):
        next_specie_details = evolution_chain.get("evolves_to")[0]
    else:
        return None
    if not next_specie_details:
        return None
    if curr_specie == pokemon:
        return next_specie_details.get("species").get("name")
    else:
        return evolve_to(pokemon, next_specie_details)


def evolve(pokemon):
    evolution_chain = get_evolution_chain(pokemon)
    evolved_pokemon = evolve_to(pokemon, evolution_chain)
    return evolved_pokemon


#print(evolve("raichu"))
