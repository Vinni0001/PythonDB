from dataclasses import dataclass
from Models.shared import db
from flask import request, jsonify
from sqlalchemy import exc
from isbnlib import is_isbn10, is_isbn13, clean


@dataclass
class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100))
    cost = db.Column(db.Float)
    stock = db.Column(db.Integer)
    isbn = db.Column(db.String(17), unique=True)
    
    book_orders_id_link = db.relationship('Book_Order', back_populates = 'book_id_fk')
    book_author_id_link = db.relationship('Book_Author', back_populates = 'book_id_fk')
    book_genre_id_link = db.relationship('Book_Genre', back_populates = 'book_id_fk')

    @property
    def serialize(self):
        return{"id":self.id,
               "title":self.title,
               "cost":self.cost,
               "stock":self.stock,
               "isbn":self.isbn}
    
    def book_availibility(request_id, request_quantity):
        return Book.query.filter_by(id=request_id).first().stock >= int(request_quantity)
        
    def update_stock(request_id, request_quantity):
        Book.query.filter_by(id=request_id).update(dict(stock = Book.stock - int(request_quantity)))


def show_books():
    result = Book.query.all()
    return jsonify([r.serialize for r in result]), 200

 
def isbn_validator(isbn):
    isbn = clean(isbn)
    if (is_isbn10(isbn) or is_isbn13(isbn)) != True:
        print(is_isbn10(isbn), is_isbn13(isbn))
        return 'invalid'
    else:
        pass
    
def new_book():
      
      if not request.form['title'] or not request.form['cost'] or not request.form['stock'] or not request.form['isbn']:
        return 'Error, Please enter all the fields', 400
      
      elif isbn_validator(request.form['isbn']) == 'invalid':
        return 'Error, invalid isbn', 400

      else:
         try:
            book = Book(title = request.form['title'], cost = request.form['cost'], stock = request.form['stock'], isbn = request.form['isbn'])
            db.session.add(book)
            db.session.commit()
            return 'Added', 200

         except exc.IntegrityError:
             return 'Error, this book already exists', 400
         

def edit_book(id):
    book = Book.query.get(id)
    for field, value in request.form.items():
        cmd = f"book.{field} = '{value}'"
        print(cmd)
        exec(cmd)
        db.session.commit()
    return "Updated field", 200

def del_book(id):
    book = Book.query.get(id)
    db.session.delete(book)
    db.session.commit()
    return 'Deleted', 200