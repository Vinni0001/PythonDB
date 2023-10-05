from flask import request, jsonify
from dataclasses import dataclass
from sqlalchemy import exc
from Models.shared import db

@dataclass
class Book_Genre(db.Model):
    __tablename__ = 'book_genre'
    id = db.Column(db.Integer, primary_key = True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.id'))

    genre_id_fk = db.relationship('Genre', back_populates='book_genre_id_link')
    book_id_fk = db.relationship('Book', back_populates='book_genre_id_link')

    @property
    def serialize(self):
        return{"id":self.id,
               "book_id":self.book_id,
               "genre_id":self.genre_id}
    
    

def show_book_genres():
    result = Book_Genre.query.all()
    return jsonify([r.serialize for r in result]), 200

 

def new_book_genre():
      
      if not request.form['book_id'] or not request.form['genre_id']:

         return 'Error, Please enter all the fields', 400

      else:
         try:
            book_genre = Book_Genre(book_id = request.form['book_id'], genre_id = request.form['genre_id'])
            db.session.add(book_genre)
            db.session.commit()
            return 'Added', 200

         except exc.IntegrityError:
             return "Error, book_genre doesn't exist", 400
         

def edit_book_genre(id):
    book_order = Book_Genre.query.get(id)
    for field, value in request.form.items():
        cmd = f"Book_Genre.{field} = '{value}'"
        print(cmd)
        exec(cmd)
        db.session.commit()
    return "Updated field", 200

def del_book_genre(id):
    book_genre = Book_Genre.query.get(id)
    db.session.delete(book_genre)
    db.session.commit()
    return 'Deleted', 200








