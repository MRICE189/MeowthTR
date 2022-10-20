# controllers.py
import json
from flask_app import app, bcrypt
from flask import render_template,redirect,request,session,flash, jsonify
from flask_app.models.model_pokemon import Pokemon

@app.route('/fill_db', methods = ['POST'])
def fill_db():
    data = request.get_json()
    for pokemon in data:
        pokemon_added = Pokemon.add_pokemon(pokemon)
        pokemon_sprite_added = Pokemon.add_sprites(pokemon)
    return jsonify(data)

