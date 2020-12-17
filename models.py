from sqlalchemy import Column, String, create_engine
from flask_sqlalchemy import SQLAlchemy, Model
from sqlalchemy import Integer, Column
import json
import os
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import SecureForm

database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()
    return db


class Car(db.Model):  
  __tablename__ = 'car'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), nullable = False)
  image_url = db.Column(db.String(250), nullable = False)
  endpoint = db.Column(db.String(250), nullable = False)
  category = db.Column(db.String(250), nullable = False)
  documents = db.relationship('Document', backref = 'car', passive_deletes = True, lazy = True)
  
  def __repr__(self):
    return f'{self.name}'

  def __init__(self, name, image_url, endpoint, category):
    self.name = name
    self.image_url = image_url
    self.endpoint = endpoint
    self.category = category
  
  def insert(self):
    db.session.add(self)
    db.session.commit() 
  
  def update(self):
    db.session.commit()
  
  def delete(self):
    db.session.delete(self)
    db.session.commit()
  
  def format(self):
    return {
    'id': self.id,
    'name': self.name,
    'image_url': self.image_url,
    'endpoint': self.endpoint,
    'category': self.category
    }

class CarView(ModelView):
    column_hide_backrefs = True
    can_export = True
    column_exclude_list = ['documents']
    column_searchable_list = ['name']
    create_modal = True
    edit_modal = True
    form_choices = {
    'category': [
        ('Autos', 'Autos'),
        ('EVs', 'EVs'),
        ('SUVs', 'SUVs'),
        ('Pickups', 'Pickups'),
        ('LCVs', 'LCVs')
    ]
}
    

class Document(db.Model):
    __tablename__= 'document'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    url = db.Column(db.String(250), nullable = False)
    image_url = db.Column(db.String(250), nullable = False)
    doc_type = db.Column(db.String(250), nullable = False)
    car_id = db.Column(db.Integer, db.ForeignKey('car.id', ondelete = 'CASCADE'), nullable = False)

    def __repr__(self):
      return f'{self.name}'


    def __init__(self, name, url, image_url, doc_type, car_id):
      self.name = name
      self.url = url
      self.image_url = image_url
      self.doc_type = doc_type
      self.car_id = car_id

    def insert(self):
      db.session.add(self)
      db.session.commit()
  
    def update(self):
      db.session.commit()

    def delete(self):
      db.session.delete(self)
      db.session.commit()

    def format(self):
      return {
      'id': self.id,
      'name': self.name,
      'url': self.url,
      'image_url': self.image_url,
      'doc_type': self.doc_type,
      'car_id': self.car_id
      }