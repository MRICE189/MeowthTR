from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app, DATABASE
from flask import session
from flask_app.models import model_pokemon

class Guess:
    def __init__(self, data):
        self.id = data['id']
        self.guess_num = data['guess_num']
        self.user_id = data['user_id']
        self.game_id = data['game_id']
        self.pokemon_id = data['pokemon_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def guess(cls, data):
        query = 'INSERT INTO guesses (guess_num, user_id, game_id, pokemon_id) VALUES (%(guess_num)s, %(user_id)s, %(game_id)s, %(pokemon_id)s);'
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def get_guesses(cls, data):
        query = 'SELECT * from guesses WHERE game_id = %(game_id)s;'
        guesses_from_db = connectToMySQL(DATABASE).query_db(query, data)
        if not guesses_from_db:
            return []
        guesses = []
        for guess in guesses_from_db:
            guess_actual = cls(guess)
            guesses.append(guess_actual)
        return guesses

    @classmethod
    def delete_guesses(cls, data):
        query = 'DELETE FROM guesses WHERE user_id = %(user_id)s AND game_id != %(game_id)s;'
        return connectToMySQL(DATABASE).query_db(query, data)

