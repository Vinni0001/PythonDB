from flask import request, jsonify
from dataclasses import dataclass
from sqlalchemy import exc
from Models.shared import db

@dataclass
class Book_Order(db.Model):
    __tablename__ = 'book_order'
    id = db.Column(db.Integer, primary_key = True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    due_date = db.Column(db.Date)
    return_date = db.Column(db.Date)
    order_id_fk = db.relationship('Order', back_populates='book_orders_id_link')
    book_id_fk = db.relationship('Book', back_populates='book_orders_id_link')

    @property
    def serialize(self):
        return{"id":self.id,
               "book_id":self.book_id,
               "order_id":self.order_id,
               "due_date":self.due_date,
               "return_date":self.return_date}
    
    

def show_book_orders():
    result = Book_Order.query.all()
    return jsonify([r.serialize for r in result]), 200

 

def new_book_order():
      
      if not request.form['book_id'] or not request.form['order_id'] or not request.form['due_date'] or not request.form['return_date']:

         return 'Error, Please enter all the fields', 400

      else:
         try:
            book_order = Book_Order(book_id = request.form['book_id'], order_id = request.form['order_id'], 
                                    due_date = request.form['due_date'], return_date = request.form['return_date'])
            db.session.add(book_order)
            db.session.commit()
            return 'Added', 200

         except exc.IntegrityError:
             return "Error, book_order doesn't exist", 400
         

def edit_book_order(id):
    book_order = Book_Order.query.get(id)
    for field, value in request.form.items():
        cmd = f"Book_Order.{field} = '{value}'"
        print(cmd)
        exec(cmd)
        db.session.commit()
    return "Updated field", 200

def del_book_order(id):
    book_order = Book_Order.query.get(id)
    db.session.delete(book_order)
    db.session.commit()
    return 'Deleted', 200








