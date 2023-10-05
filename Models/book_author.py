from flask import request, jsonify
from dataclasses import dataclass
from sqlalchemy import exc
from Models.shared import db

@dataclass
class Book_Author(db.Model):
    __tablename__ = 'book_author'
    id = db.Column(db.Integer, primary_key = True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))

    author_id_fk = db.relationship('Author', back_populates='book_author_id_link')
    book_id_fk = db.relationship('Book', back_populates='book_author_id_link')

    @property
    def serialize(self):
        return{"id":self.id,
               "book_id":self.book_id,
               "author_id":self.author_id}
    
    

def show_book_authors():
    result = Book_Author.query.all()
    return jsonify([r.serialize for r in result]), 200

 

def new_book_author():
      
      if not request.form['book_id'] or not request.form['author_id']:

         return 'Error, Please enter all the fields', 400

      else:
         try:
            book_author = Book_Author(book_id = request.form['book_id'], author_id = request.form['author_id'])
            db.session.add(book_author)
            db.session.commit()
            return 'Added', 200

         except exc.IntegrityError:
             return "Error, book_author doesn't exist", 400
         

def edit_book_author(id):
    book_order = Book_Author.query.get(id)
    for field, value in request.form.items():
        cmd = f"Book_Author.{field} = '{value}'"
        print(cmd)
        exec(cmd)
        db.session.commit()
    return "Updated field", 200

def del_book_author(id):
    book_author = Book_Author.query.get(id)
    db.session.delete(book_author)
    db.session.commit()
    return 'Deleted', 200








