from connection import get_db
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from connection import Base
import random
from user import User


class Pokemon(Base):
    __tablename__ = 'pokemondata'

    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String(512))
    type_1 = Column(String(512))
    type_2 = Column(String(512))
    generation = Column(Integer)
    legendary = Column(Boolean)
    total = Column(Integer)
    hp = Column(Integer)
    attack = Column(Integer)
    defense = Column(Integer)
    sp_atk = Column(Integer)
    sp_def = Column(Integer)
    speed = Column(Integer)
    icon_name = Column(String(512))

    favorites = relationship("Favorite", back_populates="pokemon", primaryjoin="Pokemon.id == Favorite.pokemon_id")
    collection = relationship("Collection", back_populates="pokemon", primaryjoin="Pokemon.id == Collection.pokemon_id")

    def __init__(self, id, name, type_1, type_2, generation, legendary, total, hp, attack, defense, sp_atk, sp_def, speed, icon_name):
        self.id = id
        self.name = name
        self.type_1 = type_1
        self.type_2 = type_2
        self.generation = generation
        self.legendary = bool(legendary)
        self.total = total
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.sp_atk = sp_atk
        self.sp_def = sp_def
        self.speed = speed
        self.icon_name = icon_name

class Pokedex:
    def __init__(self):
        self.load_data()

    def load_data(self):
        with get_db() as db:
            pokemon_list = db.query(Pokemon).order_by(Pokemon.id).all()
            self.pokemon_list = pokemon_list

    def get_all_pokemon(self):
        return self.pokemon_list

    def get_pokemon_by_name(self, name):
        for pokemon in self.pokemon_list:
            if pokemon.name.lower() == name.lower():
                return pokemon
        return None
    
    def get_pokemon_by_search(self, name: str):
        if len(name) < 3:
            return []
        
        matching_pokemon = [pokemon for pokemon in self.pokemon_list if name.lower() in pokemon.name.lower()]
        return matching_pokemon

    def get_pokemon_by_id(self, id):
        id = str(id)
        for pokemon in self.pokemon_list:
            if str(pokemon.id) == id:
                return pokemon
        return None
    
    def get_pokemon_by_type1(self, type_1):
        matching_pokemon = []
        for pokemon in self.pokemon_list:
            if pokemon.type_1.lower() == type_1.lower():
                matching_pokemon.append(pokemon)
        return matching_pokemon
    
    # Could use list comprehension instead
    # def get_pokemon_by_type1(self, type1):
    # return [pokemon for pokemon in self.pokemon_list if pokemon.type1.lower() == type1.lower()]
    
    def get_pokemon_by_type2(self, type_2):
        matching_pokemon = []
        for pokemon in self.pokemon_list:
            if pokemon.type_2.lower() == type_2.lower():
                matching_pokemon.append(pokemon)
        return matching_pokemon
    
    def get_pokemon_by_type(self, type):
        matching_pokemon = []
        for pokemon in self.pokemon_list:
            if pokemon.type_1.lower() == type.lower() or pokemon.type_2.lower() == type.lower():
                matching_pokemon.append(pokemon)
        return matching_pokemon
    
    def get_pokemon_by_generation(self, generation):
        matching_pokemon = []
        for pokemon in self.pokemon_list:
            if pokemon.generation == generation:
                matching_pokemon.append(pokemon)
        return matching_pokemon
    
    def get_pokemon_by_legendary(self):
        legendary_pokemon = []
        for pokemon in self.pokemon_list:
            if pokemon.legendary == True or pokemon.legendary == "True":
                legendary_pokemon.append(pokemon)
        return legendary_pokemon
    
    def get_random_team(self):
        team_size = 6
        random_team = random.sample(self.pokemon_list, team_size)
        return random_team
    
    def get_strong_team(self):
        team_size = 6

        total_stats = [pokemon.total for pokemon in self.pokemon_list]

        cutoff = int(len(total_stats) * 0.2)
        top_pokemon_indices = sorted(range(len(total_stats)), key=lambda i: total_stats[i], reverse=True)[:cutoff]

        sorted_top_pokemon_indices = sorted(top_pokemon_indices)
        strong_team = random.sample([self.pokemon_list[i] for i in sorted_top_pokemon_indices], k=team_size)
        return strong_team
    
    def get_weak_team(self):
        team_size = 6

        total_stats = [pokemon.total for pokemon in self.pokemon_list]

        cutoff = int(len(total_stats) * 0.2)
        lowest_pokemon_indices = sorted(range(len(total_stats)), key=lambda i: total_stats[i])[:cutoff]

        sorted_lowest_pokemon_indices = sorted(lowest_pokemon_indices)
        weak_team_indices = random.sample(sorted_lowest_pokemon_indices, k=team_size)
        weak_team = [self.pokemon_list[i] for i in weak_team_indices]
        return weak_team
    
    def get_legendary_team(self):
        team_size = 6

        legendary_pokemon = [pokemon for pokemon in self.pokemon_list if pokemon.legendary == True or pokemon.legendary == "True"]

        team = random.sample(legendary_pokemon, k=team_size)
        return team
    
    def get_rainbow_team(self):
        team = []

        fire_pokemon = random.choice(self.get_pokemon_by_type1("Fire"))
        team.append(fire_pokemon)

        fighting_ground_pokemon = random.choice(self.get_pokemon_by_type1("Fighting") + self.get_pokemon_by_type1("Ground"))
        team.append(fighting_ground_pokemon)

        electric_pokemon = random.choice(self.get_pokemon_by_type1("Electric"))
        team.append(electric_pokemon)

        grass_pokemon = random.choice(self.get_pokemon_by_type1("Grass"))
        team.append(grass_pokemon)

        water_pokemon = random.choice(self.get_pokemon_by_type1("Water"))
        team.append(water_pokemon)

        poison_ghost_pokemon = random.choice(self.get_pokemon_by_type1("Poison") + self.get_pokemon_by_type1("Ghost"))
        team.append(poison_ghost_pokemon)

        return team
    
class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    pokemon_id = Column(Integer, ForeignKey("pokemondata.id"))

    user = relationship("User", back_populates="favorites")
    pokemon = relationship("Pokemon", back_populates="favorites")

class Collection(Base):
    __tablename__ = "collection"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    pokemon_id = Column(Integer, ForeignKey("pokemondata.id"))

    user = relationship("User", back_populates="collection")
    pokemon = relationship("Pokemon", back_populates="collection")