import random
from fastapi import APIRouter
from api.models import Pokedex

pokedex = Pokedex()

router = APIRouter()

@router.get("/")
def get_all_pokemon():
    return pokedex.get_all_pokemon()

@router.get("/name/{name}")
def get_pokemon_by_name(name: str):
    return pokedex.get_pokemon_by_name(name)

@router.get("/search/{name}")
def get_pokemon_by_search(name: str):
    return pokedex.get_pokemon_by_search(name)

@router.get("/id/{id}")
def get_pokemon_by_id(id: str):
    return pokedex.get_pokemon_by_id(id)

@router.get("/type1/{type1}")
def get_pokemon_by_type1(type1: str):
    return pokedex.get_pokemon_by_type1(type1)

@router.get("/type2/{type2}")
def get_pokemon_by_type2(type2: str):
    return pokedex.get_pokemon_by_type2(type2)

@router.get("/type/{type}")
def get_pokemon_by_type(type: str):
    return pokedex.get_pokemon_by_type(type)

@router.get("/generation/{generation}")
def get_pokemon_by_generation(generation: int):
    return pokedex.get_pokemon_by_generation(generation)

@router.get("/legendary")
def get_pokemon_by_legendary():
    return pokedex.get_pokemon_by_legendary()

@router.get("/random")
def get_random_pokemon():
    random_pokemon = random.choice(pokedex.get_all_pokemon())
    return random_pokemon
    
@router.get("/random_team")
def get_random_team():
    return pokedex.get_random_team()

@router.get("/strong_team")
def get_strong_team():
    return pokedex.get_strong_team()

@router.get("/weak_team")
def get_weak_team():
    return pokedex.get_weak_team()

@router.get("/legendary_team")
def get_legendary_team():
    return pokedex.get_legendary_team()

@router.get("/rainbow_team")
def get_rainbow_team():
    return pokedex.get_rainbow_team()