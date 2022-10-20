# controllers.py
from flask_app import app
from flask import render_template,redirect,request,session,flash,jsonify, json
from flask_app.models.model_user import User
from flask_app.models.model_pokemon import Pokemon
from flask_app.models.model_game import Game
from flask_app.models.model_guess import Guess
import random

@app.route('/main')
def main():
    if 'uuid' not in session:
        return redirect('/')
    return render_template('main_page.html')

@app.route('/scores')
def scores():
    if 'uuid' not in session:
        return redirect('/')
    context = {
        'games': Game.get_all_wins({'user_id': session['uuid']})
    }
    return render_template('scores.html', **context)

@app.route('/new_game')
def new_game():
    if 'in_prog' not in session:
        pokemon_num = random.randint(1,649)
        target = Pokemon.get_one_pokemon({'poke_id': pokemon_num})
        session['pokemon_id'] = pokemon_num
        start_data = {
            'user_id': session['uuid'],
            'pokemon_id': pokemon_num
        }
        game = Game.start_game(start_data)
        session['in_prog'] = game
        old_guesses = Guess.delete_guesses({
            'user_id': session['uuid'],
            'game_id': session['in_prog']
        })
    return redirect('/play')


@app.route('/play')
def play():
    if 'uuid' not in session:
        return redirect('/')
    if 'in_prog' not in session:
        return redirect('/main')
    context = {
        'all_pokemon': Pokemon.get_all_pokemon(),
        'game': Game.get_target_of_game({
            'user_id': session['uuid'],
            'game_id': session['in_prog'],
        }),
        'comparisons': []
    }
    target = Pokemon.get_one_pokemon({'poke_id': session['pokemon_id']})
    guesses = Guess.get_guesses({'game_id': session['in_prog']}),
    
    for guess in guesses[0]:
        comparison = {}
        guess_mon = Pokemon.get_one_pokemon({'poke_id': guess.pokemon_id})

        if target.poke_name == guess_mon.poke_name:
            comparison['comp_name'] = f'<td class="text-success">{guess_mon.poke_name.capitalize()}</td>'
        else:
            comparison['comp_name'] = f'<td class="text-danger">{guess_mon.poke_name.capitalize()}</td>'
        
        comparison['poke_sprite'] = f'<td><img src="{guess_mon.poke_sprite}" class="sprite"></td>'

        if int(target.poke_gen) == int(guess_mon.poke_gen):
            comparison['comp_gen'] = '<td><img class="icon" src="../static/img/check.png"></td>'
        if int(target.poke_gen) > int(guess_mon.poke_gen):
            comparison['comp_gen'] = '<td><img class="icon" src="../static/img/up.png"></td>'
        if int(target.poke_gen) < int(guess_mon.poke_gen):
            comparison['comp_gen'] = '<td><img class="icon" src="../static/img/down.png"></td>'

        print(target.poke_type1, guess_mon.poke_type1)
        if target.poke_type1 == guess_mon.poke_type1:
            comparison['comp_type1'] = f'<td class="text-success">{guess_mon.poke_type1.capitalize()}</td>'
        else:
            comparison['comp_type1'] = f'<td class="text-danger">{guess_mon.poke_type1.capitalize()}</td>'
        if target.poke_type2 == guess_mon.poke_type2:
            comparison['comp_type2'] = f'<td class="text-success">{guess_mon.poke_type2.capitalize()}</td>'
        else:
            comparison['comp_type2'] = f'<td class="text-danger">{guess_mon.poke_type2.capitalize()}</td>'
        
        if int(target.poke_att) == int(guess_mon.poke_att):
            comparison['comp_att'] = '<td><img class="icon" src="../static/img/check.png"></td>'
        elif int(target.poke_att) > int(guess_mon.poke_att):
            comparison['comp_att'] = '<td><img class="icon" src="../static/img/up.png"></td>'
        elif int(target.poke_att) < int(guess_mon.poke_att):
            comparison['comp_att'] = '<td><img class="icon" src="../static/img/down.png"></td>'

        if int(target.poke_satt) == int(guess_mon.poke_satt):
            comparison['comp_satt'] = '<td><img class="icon" src="../static/img/check.png"></td>'
        elif int(target.poke_satt) > int(guess_mon.poke_satt):
            comparison['comp_satt'] = '<td><img class="icon" src="../static/img/up.png"></td>'
        elif int(target.poke_satt) < int(guess_mon.poke_satt):
            comparison['comp_satt'] = '<td><img class="icon" src="../static/img/down.png"></td>'

        if int(target.poke_height) == int(guess_mon.poke_height):
            comparison['comp_height'] = '<td><img class="icon" src="../static/img/check.png"></td>'
        elif int(target.poke_height) > int(guess_mon.poke_height):
            comparison['comp_height'] = '<td><img class="icon" src="../static/img/up.png"></td>'
        elif int(target.poke_height) < int(guess_mon.poke_height):
            comparison['comp_height'] = '<td><img class="icon" src="../static/img/down.png"></td>'

        if int(target.poke_weight) == int(guess_mon.poke_weight):
            comparison['comp_weight'] = '<td><img class="icon" src="../static/img/check.png"></td>'
        elif int(target.poke_weight) > int(guess_mon.poke_weight):
            comparison['comp_weight'] = '<td><img class="icon" src="../static/img/up.png"></td>'
        elif int(target.poke_weight) < int(guess_mon.poke_weight):
            comparison['comp_weight'] = '<td><img class="icon" src="../static/img/down.png"></td>'

        context['comparisons'].append(comparison)
    return render_template('play.html',**context)

@app.route('/end')
def end_game():
    if 'in_prog' in session:
        del session['in_prog']
    if 'guess_num' in session:
        del session['guess_num']
    if 'pokemon_id' in session:
        del session['pokemon_id']
    return redirect('/main')

@app.route('/api/win', methods=['POST'])
def win():
    win_data = {
        'guesses': session['guess_num'],
        'user_id': session['uuid'],
        'game_id': session['in_prog']
    }
    Game.win_game(win_data)
    old_guesses = Guess.delete_guesses({
        'user_id': session['uuid'],
        'game_id': session['in_prog']
        })
    Game.delete_lost_games({'user_id': session['uuid']})
    del session['in_prog']
    del session['guess_num']
    del session['pokemon_id']
    return jsonify({'msg': 'You win!'})

@app.route('/api/lose', methods=['POST'])
def lose():
    if 'uuid'  in session:
        old_guesses = Guess.delete_guesses({
            'user_id': session['uuid'],
            'game_id': session['in_prog']
        })
        if 'in_prog' in session:
            del session['in_prog']
        if 'guess_num' in session:
            del session['guess_num']
        if 'pokemon_id' in session:
            del session['pokemon_id']
        Game.delete_lost_games({'user_id': session['uuid']})
    return jsonify({'msg': 'You lose'})

