from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app, DATABASE
from flask import session
from flask_app.models import model_pokemon

class Game:
    def __init__(self, data):
        self.id = session['uuid']
        self.user_id = data['user_id']
        self.pokemon_id = data['pokemon_id']
        self.guesses = data['guesses']
        self.win = data['win']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def start_game(cls, data):
        query = 'INSERT INTO games (user_id, pokemon_id, guesses, win) VALUES (%(user_id)s, %(pokemon_id)s, 0, "no");'
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_target_of_game(cls, data):
        query = 'SELECT * FROM games LEFT JOIN pokemons ON pokemon_id = pokemons.poke_id WHERE user_id = %(user_id)s and games.id = %(game_id)s;'
        result = connectToMySQL(DATABASE).query_db(query, data)
        game = cls(result[0])
        target_data = {
            **result[0],
            'created_at': result[0]['pokemons.created_at'],
            'updated_at': result[0]['pokemons.updated_at']
        }
        game.target = model_pokemon.Pokemon(target_data)
        return game
    
    @classmethod
    def get_all_wins(cls, data):
        query = 'SELECT * FROM games LEFT JOIN pokemons ON pokemon_id = pokemons.poke_id WHERE user_id = %(user_id)s and win = "yes";'
        games_from_db = connectToMySQL(DATABASE).query_db(query, data)
        if not games_from_db:
            return []
        games = []
        for game in games_from_db:
            game_actual = cls(game)
            target_data = {
                **game,
                'created_at': game['pokemons.created_at'],
                'updated_at': game['pokemons.updated_at']
            }
            game_actual.target = model_pokemon.Pokemon(target_data)
            games.append(game_actual)
        return games

    @classmethod
    def win_game(cls, data):
        query = 'UPDATE games SET guesses = %(guesses)s, win = "yes" WHERE user_id = %(user_id)s AND id = %(game_id)s;'
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def delete_lost_games(cls,data):
        query = 'DELETE FROM games WHERE user_id = %(user_id)s AND win = "no";'
        return connectToMySQL(DATABASE).query_db(query, data)