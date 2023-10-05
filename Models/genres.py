from flask import request, jsonify
from dataclasses import dataclass
from sqlalchemy import exc
from Models.shared import db

@dataclass
class Genre(db.Model):
    __tablename__ = 'genres'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(100))

    book_genre_id_link = db.relationship('Book_Genre', back_populates = 'genre_id_fk')

    @property
    def serialize(self):
        return{"id":self.id,
               "name":self.name,
               "description":self.description}
    
    

def show_genres():
    result = Genre.query.all()
    return jsonify([r.serialize for r in result]), 200

 

def new_genre():
      
      if not request.form['name'] or not request.form['description']:

         return 'Error, Please enter all the fields', 400

      else:
         try:
            genre = Genre(name = request.form['name'], description = request.form['description'])
            db.session.add(genre)
            db.session.commit()
            return 'Added', 200

         except exc.IntegrityError:
             return "Error, genre doesn't exist", 400
         

def edit_genre(id):
    genre = Genre.query.get(id)
    for field, value in request.form.items():
        cmd = f"genre.{field} = '{value}'"
        print(cmd)
        exec(cmd)
        db.session.commit()
    return "Updated field", 200

def del_genre(id):
    genre = Genre.query.get(id)
    db.session.delete(genre)
    db.session.commit()
    return 'Deleted', 200








