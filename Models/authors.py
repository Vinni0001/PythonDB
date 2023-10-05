from flask import request, jsonify
from dataclasses import dataclass
from sqlalchemy import exc
from Models.shared import db

@dataclass
class Author(db.Model):
    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    
    book_author_id_link = db.relationship('Book_Author', back_populates = 'author_id_fk')

    @property
    def serialize(self):
        return {
            "id":self.id,
            "first_name":self.first_name,
            "last_name":self.last_name
        }
    
    

def show_authors():
    result = Author.query.all()
    return jsonify([r.serialize for r in result]), 200

 

def new_author():
      
      if not request.form['first_name'] or not request.form['last_name']:

         return 'Error, Please enter all the fields', 400

      else:
         try:
            author = Author(first_name = request.form['first_name'], last_name = request.form['last_name'])
            db.session.add(author)
            db.session.commit()
            return 'Added', 200

         except exc.IntegrityError:
             return "Error, author doesn't exist", 400
         

def edit_author(id):
    author = Author.query.get(id)
    for field, value in request.form.items():
        cmd = f"author.{field} = '{value}'"
        print(cmd)
        exec(cmd)
        db.session.commit()
    return "Updated field", 200

def del_author(id):
    author = Author.query.get(id)
    db.session.delete(author)
    db.session.commit()
    return 'Deleted', 200








