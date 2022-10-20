from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app, bcrypt, DATABASE
from flask import flash, session

class Pokemon:
    def __init__(self, data):
        self.poke_id = data['poke_id']
        self.poke_name = data['poke_name']
        self.poke_gen = data['poke_gen']
        self.poke_sprite = data['poke_sprite']
        self.poke_type1 = data['poke_type1']
        self.poke_type2 = data['poke_type2']
        self.poke_att = data['poke_att']
        self.poke_satt = data['poke_satt']
        self.poke_height = data['poke_height']
        self.poke_weight = data['poke_weight']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def add_pokemon(cls, data):
        query = 'INSERT INTO pokemons (poke_id, poke_name, poke_gen, poke_type1, poke_type2, poke_att, poke_satt, poke_height, poke_weight) VALUES (%(poke_id)s, %(poke_name)s, %(poke_gen)s, %(poke_type1)s, %(poke_type2)s, %(poke_att)s, %(poke_satt)s, %(poke_height)s, %(poke_weight)s);'
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def add_sprites(cls,data):
        query = 'UPDATE pokemons SET poke_sprite = %(poke_sprite)s WHERE poke_id = %(poke_id)s;'
        pokemon = connectToMySQL(DATABASE).query_db(query, data)
        return pokemon

    @classmethod
    def get_all_pokemon(cls):
        query = 'SELECT * FROM pokemons;'
        pokemon_from_db = connectToMySQL(DATABASE).query_db(query)
        if not pokemon_from_db:
            return []
        pokemon = []
        for dict in pokemon_from_db:
            pokemon.append(dict)
        return pokemon

    @classmethod
    def get_one_pokemon(cls, data):
        query = 'SELECT * FROM pokemons WHERE poke_id = %(poke_id)s;'
        pokemon = connectToMySQL(DATABASE).query_db(query, data)
        if not pokemon:
            return False
        return cls(pokemon[0])
    
    @classmethod
    def get_one_pokemon_by_name(cls, data):
        query = 'SELECT * FROM pokemons WHERE poke_name = %(poke_name)s;'
        pokemon = connectToMySQL(DATABASE).query_db(query, data)
        if not pokemon:
            return False
        return cls(pokemon[0])