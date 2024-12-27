from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

user_favorites=db.Table(
    'user_favorites',
    db.Column("user_id",db.Integer,db.ForeignKey("user.id")),
    db.Column("favorites_id",db.Integer, db.ForeignKey("favorite.id"))
)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), nullable=False, unique=True)
    password = db.Column(db.String(10), nullable=False)

    favorite=db.relationship("Favorite", secondary=user_favorites ,back_populates="user")
    
    def serialize(self):
        return{
            "id":self.id,
            "username":self.username,
            "favorites":[favorite.serialize() for favorite in self.favorite]
        }

   


class Planet(db.Model):
    __tablename__ = 'planet'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(250),nullable=False)
    climate = db.Column(db.String(50))


    def serialize(self):
        return{
            "id":self.id,
            "name":self.name,
            "description":self.description,
            "climate":self.climate
        }

   
    


class Character(db.Model):
    __tablename__='character'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50),nullable=False)
    alive = db.Column(db.Boolean,nullable=False)


    def serialize(self):
        return{
            "id":self.id,
            "name":self.name,
            "alive":self.alive
        }

class Favorite(db.Model):
    __tablename__='favorite'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    character_id = db.Column(db.Integer,db.ForeignKey('character.id'))
    planet_id = db.Column(db.Integer,db.ForeignKey('planet.id'))

    user = db.relationship('User', secondary=user_favorites, back_populates="favorite")

    def serialize(self):
        return{
            "user_id": self.user_id,
            "character_id":self.character_id,
            "planet_id":self.planet_id
        }