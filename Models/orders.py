from flask import request, jsonify
from dataclasses import dataclass
from sqlalchemy import exc
from Models.shared import db
from Models.book_service import *

@dataclass
class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key = True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    order_date = db.Column(db.Date)
    total_price = db.Column(db.Float)
    customer_id_link = db.relationship('Customer', back_populates = 'orders')
    book_orders_id_link = db.relationship('Book_Order', back_populates = 'order_id_fk')
    

    @property
    def serialize(self):
        return{"id":self.id,
               "customer_id":self.customer_id,
               "order_date":self.order_date,
               "total_price":self.total_price}
    

def show_orders():
    result = Order.query.all()
    return jsonify([r.serialize for r in result]), 200

 

def new_order():
      
    if not request.form['customer_id'] or not request.form['order_date'] or not request.form['total_price']:

        return 'Error, Please enter all the fields', 400

      
    try:
        if Book_service.show_stock() == True or Book_service.edit_stock() == False:
            return "Not enough stock", 400
        
        order = Order(customer_id = request.form['customer_id'], order_date = request.form['order_date'], total_price = request.form['total_price'])
        db.session.add(order)
        db.session.commit()
        return 'Added', 200

    except exc.IntegrityError:
        return "Error, customer doesn't exist", 400
         

def edit_order(id):
    order = Order.query.get(id)
    for field, value in request.form.items():
        cmd = f"order.{field} = '{value}'"
        print(cmd)
        exec(cmd)
        db.session.commit()
    return "Updated field", 200

def del_order(id):
    order = Order.query.get(id)
    db.session.delete(order)
    db.session.commit()
    return 'Deleted', 200








