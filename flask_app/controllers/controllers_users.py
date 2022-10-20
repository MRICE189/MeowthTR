# controllers.py
from flask_app import app, bcrypt
from flask import render_template,redirect,request,session,flash
from flask_app.models.model_user import User

@app.route('/')
def index():
    if 'uuid' in session:
        return redirect('/main')
    return render_template('index.html')

@app.route('/create')
def create_page():
    return render_template('create_user.html')

@app.route('/login')
def login_page():
    return render_template('login_user.html')

@app.route('/users/register', methods=['POST'])
def create_user():
    if not User.validate_user(request.form):
        return redirect('/create')
    hash_pw = bcrypt.generate_password_hash(request.form['pw'])
    data = {
        **request.form,
        'pw': hash_pw
    }
    print(data)
    user_id = User.create_user(data)
    print(user_id)
    session['uuid'] = user_id
    return redirect('/main')
    
@app.route('/users/login', methods=['POST'])
def login():
    if not User.validate_login(request.form):
        return redirect('/login')
    return redirect('/main')

@app.route('/logout')
def logout():
    if 'uuid' in session:
        del session['uuid']
    if 'in_prog' in session:
        del session['in_prog']
    if 'pokemon_id' in session:
        del session['pokemon_id']
    if 'guess_num' in session:
        del session['guess_num']
    return redirect('/')
