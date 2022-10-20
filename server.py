from flask_app.controllers import controllers_routes, controllers_users, controllers_pokemon, controllers_guesses
from flask_app import app

if __name__=="__main__":
    app.run(debug=True)  