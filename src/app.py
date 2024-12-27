"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character,Planet,Favorite

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():
    return generate_sitemap(app)



# Get char 1
@app.route('/characters', methods=['GET'])
def get_all_characters():
    characters = Character.query.all()
    return jsonify({
        "characters": list(map(lambda item: item.serialize(), characters))
    }),200

# 2 
@app.route('/character/<int:theid>', methods=['GET'])
def get_character(theid):
    character = Character.query.get(theid)
    if character is None:
        return jsonify("Character doesn't exists"),404
    else:
        return jsonify(character.serialize()),200

#Get planets
@app.route('/planets', methods=['GET'])
def get_all_planets():
    planets=Planet.query.all()
    return jsonify({
        "planets":list(map(lambda item: item.serialize(),planets))
    })

#Get one Planet
@app.route('/planet/<int:theid>', methods=['GET'])
def get_planet(theid):
    planet=Planet.query.get(theid)
    if planet is None:
        return jsonify("Planet doesnt exists"),404
    else:
        return jsonify(planet.serialize_planet()),200
    

@app.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    return({
        "users":list(map(lambda item: item.serialize(), users))
    })

@app.route('/users/favorites', methods=['GET'])
def get_favorites():
    fav = Favorite.query.all()
    return jsonify({
        "favorites":list(map(lambda item: item.serialize(),fav))
    }),200



@app.route('/favorite/planet/<int:id_planet>', methods=['POST'])
def add_favorite_planet(id_planet):
 
    fav = Favorite()
    try:
        planet = Planet.query.get(id_planet)

        if planet is not None:
            fav.user_id=1
            fav.id_planet=id_planet

            db.session.add(fav)
            db.session.commit()
        
            return jsonify("Saved")
        else:
            return jsonify(f"Planet {id_planet} not registered, try later ")
    
    except Exception as error:
        return jsonify(f"Server Error{error.args}"),500


@app.route('/favorite/character/<int:character_id>', methods=['POST'])
def add_favorite_character(character_id):
 
    fav = Favorite()
    try:
        character = Character.query.get(character_id)

        if character is not None:
            fav.user_id=2
            fav.character_id=character_id

            db.session.add(fav)
            db.session.commit()
        
            return jsonify("Saved")
        else:
            return jsonify(f"Planet {character_id} not registered, try later ")
    
    except Exception as error:
        return jsonify(f"Server Error{error.args}"),500


@app.route('/favorite/planet/<int:id_planet>', methods=['DELETE'])
def delete_planet(id_planet):
    fav = Favorite.query.filter_by(planet_id=id_planet).first()
    if fav is None:
        return jsonify(f'Planet {id_planet} doesnt exists'),404
    else:
        try:
            db.session.delete(fav)
            db.session.commit()
            return jsonify('Deleted'),200

        except Exception as error:
            return jsonify(f"Server Error{error.args}"),500
        
@app.route('/favorite/character/<int:id_character>', methods=['DELETE'])
def delete_character(id_character):
    fav = Favorite.query.filter_by(character_id=id_character).first()
    if fav is None:
        return jsonify(f'Character {id_character} doesnt exists'),404
    else:
        try:
            db.session.delete(fav)
            db.session.commit()
            return jsonify('Deleted'),200

        except Exception as error:
            return jsonify(f"Server Error{error.args}"),500




if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
