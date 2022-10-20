# controllers.py
from flask_app import app, bcrypt
from flask import render_template,redirect,request,session,flash, jsonify
from flask_app.models.model_pokemon import Pokemon
from flask_app.models.model_guess import Guess
from flask_app.models.model_game import Game

@app.route ('/api/guess', methods=['POST'])
def guess():
    data = {
        'poke_name': request.form['guess'].lower()
    }
    guess = Pokemon.get_one_pokemon_by_name(data)
    if not guess:
        return jsonify({'msg': 'no data'})
    else:
        if 'guess_num' not in session:
            session['guess_num'] = 1
        else:
            session['guess_num'] += 1
        guess_data = {
            'guess_num': session['guess_num'],
            'user_id': session['uuid'],
            'game_id': session['in_prog'],
            'pokemon_id': guess.poke_id
        }
        add_guess = Guess.guess(guess_data)
        return jsonify(guess_data)

@app.route('/api/compare', methods=['POST'])
def get_target():
    game = Game.get_target_of_game({
            'user_id': session['uuid'],
            'game_id': session['in_prog'],
        })
    target = {
        'target_id': game.target.poke_id,
        'target_name': game.target.poke_name,
        'target_gen': game.target.poke_gen,
        'target_type1': game.target.poke_type1,
        'target_type2': game.target.poke_type2,
        'target_att': game.target.poke_att,
        'target_satt': game.target.poke_satt,
        'target_height': game.target.poke_height,
        'target_weight': game.target.poke_weight,
    }
    res = {
        'guess_num': session['guess_num'],
        'target_name': target['target_name']
        }
    if int(target['target_id']) == int(request.form['poke_id']):
        res['comp_name'] = 'match'
    else:
        res['comp_name'] = 'not match'

    if int(target['target_gen']) == int(request.form['poke_gen']):
        res['comp_gen'] = 'match'
    elif int(target['target_gen']) > int(request.form['poke_gen']):
        res['comp_gen'] = '^'
    elif int(target['target_gen']) < int(request.form['poke_gen']):
        res['comp_gen'] = 'v'
    
    if target['target_type1'] == request.form['poke_type1']:
        res['comp_type1'] = 'match'
    else:
        res['comp_type1'] = 'not match'
    if target['target_type2'] == request.form['poke_type2']:
        res['comp_type2'] = 'match'
    else:
        res['comp_type2'] = 'not match'

    if int(target['target_att']) == int(request.form['poke_att']):
        res['comp_att'] = 'match'
    elif int(target['target_att']) > int(request.form['poke_att']):
        res['comp_att'] = '^'
    elif int(target['target_att']) < int(request.form['poke_att']):
        res['comp_att'] = 'v'

    if int(target['target_satt']) == int(request.form['poke_satt']):
        res['comp_satt'] = 'match'
    elif int(target['target_satt']) > int(request.form['poke_satt']):
        res['comp_satt'] = '^'
    elif int(target['target_satt']) < int(request.form['poke_satt']):
        res['comp_satt'] = 'v'

    if int(target['target_height']) == int(request.form['poke_height']):
        res['comp_height'] = 'match'
    elif int(target['target_height']) > int(request.form['poke_height']):
        res['comp_height'] = '^'
    elif int(target['target_height']) < int(request.form['poke_height']):
        res['comp_height'] = 'v'

    if int(target['target_weight']) == int(request.form['poke_weight']):
        res['comp_weight'] = 'match'
    elif int(target['target_weight']) > int(request.form['poke_weight']):
        res['comp_weight'] = '^'
    elif int(target['target_weight']) < int(request.form['poke_weight']):
        res['comp_weight'] = 'v'
    
    return jsonify(res)