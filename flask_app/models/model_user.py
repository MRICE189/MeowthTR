from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app, bcrypt, DATABASE
from flask import flash, session

class User:
    def __init__(self, data):
        self.id = data['id']
        self.username = data['username']
        self.pw = data['pw']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def create_user(cls, data):
        query = 'INSERT INTO users (username, pw) VALUES (%(username)s, %(pw)s);'
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_by_username(cls, data):
        query = 'SELECT * FROM users WHERE username = %(username)s;'
        result = connectToMySQL(DATABASE).query_db(query, data)
        if not result:
            return False
        return cls(result[0])


    @staticmethod
    def validate_user(data):
        is_valid = True
        if len(data['username']) < 2:
            is_valid = False
            flash('Invalid Username', 'err_user_username')
        if len(data['pw']) < 8:
            is_valid = False
            flash('Password must be at least 8 characters long.', 'err_user_pw')
        if data['pw'] != data['confirm_pw']:
            is_valid = False
            flash('Passwords do not match!', 'err_user_match')
        if is_valid:
            potential_user = User.get_by_username({'username': data['username']})
            if potential_user:
                flash('Username already taken, sorry!', 'err_user_taken')
                is_valid = False
        return is_valid

    @staticmethod
    def validate_login(data):
        is_valid = True
        if len(data['username']) < 1:
            is_valid = False
            flash('Invalid Username', 'err_login_username')
        if len(data['pw']) < 8:
            is_valid = False
            flash('Invalid Password length.', 'err_login_pw')
        if is_valid:
            potential_user = User.get_by_username({'username': data['username']})
            if not potential_user:
                flash('Username not found', 'err_login_valid')
                is_valid = False
            else:
                if not bcrypt.check_password_hash(potential_user.pw, data['pw']):
                    flash('Invalid credentials.', 'err_login_match')
                    is_valid = False
                else:
                    session['uuid'] = potential_user.id
        return is_valid