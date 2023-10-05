from flask import request
from Models.books import Book
from Models.shared import db


class Book_service:
    def show_stock():
        book = Book.query.filter_by(id=request.form['book_id']).first()
        #print(int(book.stock) <= 0)
        if book.stock <= 0:
           return True 
        else:
           pass
    
    def edit_stock():
       if Book.book_availibility(request.form['book_id'], request.form['quantity']) == True:
          return Book.update_stock(request.form['book_id'], request.form['quantity'])
       else:
          return False
     



