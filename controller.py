from flask import Flask
from Models.customers import *
from Models.orders import *
from Models.books import *
from Models.authors import *
from Models.genres import *
from Models.book_order import *
from Models.book_author import *
from Models.book_genre import *
import os
from Models.shared import db

app = Flask (__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_POOL_RECYCLE'] = 280
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "SOMETHING"

db.init_app(app)

with app.app_context():
    db.create_all()
    

#Customers -----------------------------------------
@app.route('/customers/', methods = ['GET'])
def customer_get():
    return show_customers()

@app.route('/customers/', methods = ['POST'])
def customer_post():
    return new_customer()

@app.route('/customers/<id>', methods = ['PATCH'])
def customer_patch(id):
    return edit_customer(id)

@app.route('/customers/<id>', methods = ['DELETE'])
def customer_del(id):
    return del_customer(id)

#Orders -----------------------------------------

@app.route('/orders/', methods = ['GET'])
def order_get():
    return show_orders()

@app.route('/orders/', methods = ['POST'])
def order_post():
    return new_order()

@app.route('/orders/<id>', methods = ['PATCH'])
def order_patch(id):
    return edit_order(id)

@app.route('/orders/<id>', methods = ['DELETE'])
def order_del(id):
    return del_order(id)

#Books -----------------------------------------
@app.route('/books/', methods = ['GET'])
def book_get():
    return show_books()

@app.route('/books/', methods = ['POST'])
def book_post():
    return new_book()

@app.route('/books/<id>', methods = ['PATCH'])
def book_patch(id):
    return edit_book(id)

@app.route('/books/<id>', methods = ['DELETE'])
def book_del(id):
    return del_book(id)

#Authors -----------------------------------------
@app.route('/authors/', methods = ['GET'])
def author_get():
    return show_authors()

@app.route('/authors/', methods = ['POST'])
def author_post():
    return new_author()

@app.route('/authors/<id>', methods = ['PATCH'])
def author_patch(id):
    return edit_author(id)

@app.route('/authors/<id>', methods = ['DELETE'])
def author_del(id):
    return del_author(id)

#Genres -----------------------------------------
@app.route('/genres/', methods = ['GET'])
def genre_get():
    return show_genres()

@app.route('/genres/', methods = ['POST'])
def genre_post():
    return new_genre()

@app.route('/genres/<id>', methods = ['PATCH'])
def genre_patch(id):
    return edit_genre(id)

@app.route('/genres/<id>', methods = ['DELETE'])
def genre_del(id):
    return del_genre(id)

#Book_Order -----------------------------------------
@app.route('/book_order/', methods = ['GET'])
def book_order_get():
    return show_book_orders()

@app.route('/book_order/', methods = ['POST'])
def book_order_post():
    return new_book_order()

@app.route('/book_order/<id>', methods = ['PATCH'])
def book_order_patch(id):
    return edit_book_order(id)

@app.route('/book_order/<id>', methods = ['DELETE'])
def book_order_del(id):
    return del_book_order(id)

#Book_Author -----------------------------------------
@app.route('/book_author/', methods = ['GET'])
def book_author_get():
    return show_book_authors()

@app.route('/book_author/', methods = ['POST'])
def book_author_post():
    return new_book_author()

@app.route('/book_author/<id>', methods = ['PATCH'])
def book_author_patch(id):
    return edit_book_author(id)

@app.route('/book_author/<id>', methods = ['DELETE'])
def book_author_del(id):
    return del_book_author(id)

#Book_Genre -----------------------------------------
@app.route('/book_genre/', methods = ['GET'])
def book_genre_get():
    return show_book_genres()

@app.route('/book_genre/', methods = ['POST'])
def book_genre_post():
    return new_book_genre()

@app.route('/book_genre/<id>', methods = ['PATCH'])
def book_genre_patch(id):
    return edit_book_genre(id)

@app.route('/book_genre/<id>', methods = ['DELETE'])
def book_genre_del(id):
    return del_book_genre(id)


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=4000)