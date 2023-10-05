from dataclasses import dataclass
from Models.shared import db
from flask import request, jsonify
from sqlalchemy import exc
from email_validator import validate_email, EmailNotValidError

@dataclass
class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    orders = db.relationship('Order', back_populates='customer_id_link', lazy = 'dynamic')

    @property
    def serialize(self):
        return{"id":self.id,
               "first_name":self.first_name,
               "last_name":self.last_name,
               "email":self.email}

    



def email_validation(email):

    try:
        emailinfo = validate_email(email, check_deliverability=False)
        email = emailinfo.normalized
        return True
    except EmailNotValidError as e:
        return str(e)
    

def show_customers():
    result = Customer.query.all()
    return jsonify([r.serialize for r in result]), 200

 

def new_customer():
      
      if not request.form['first_name'] or not request.form['last_name'] or not request.form['email']:

         return 'Error, Please enter all the fields', 400

      else:
         try:
            customer = Customer(first_name = request.form['first_name'], last_name = request.form['last_name'], email = request.form['email'])

            if email_validation(request.form['email']) == True:
                db.session.add(customer)
                db.session.commit()
                return 'Added', 200
            else:
                return email_validation(request.form['email'])

         except exc.IntegrityError:
             return 'Error, this email is already in use', 400
         

def edit_customer(id):
    customer = Customer.query.get(id)
    for field, value in request.form.items():
        cmd = f"customer.{field} = '{value}'"
        print(cmd)
        exec(cmd)
        db.session.commit()
    return "Updated field", 200

def del_customer(id):
    customer = Customer.query.get(id)
    db.session.delete(customer)
    db.session.commit()
    return 'Deleted', 200