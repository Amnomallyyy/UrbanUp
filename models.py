from Final import db

from flask_login import UserMixin
class Project(db.Model):
   __tablename__ = 'project'
   id = db.Column(db.Integer,primary_key = True)
   jsonMapData = db.Column(db.Text, nullable = False)
   aiAdvice = db.Column(db.Text, unique = False,nullable = False)
   fileName = db.Column(db.Text, unique = False, nullable = False) 
   user_id = db.Column(db.Integer,db.ForeignKey('user.id'))



class User(db.Model, UserMixin):
   __tablename__ = "user"
   id = db.Column(db.Integer, primary_key = True)
   email = db.Column(db.Text, unique = True)
   firstname = db.Column(db.Text)
   password = db.Column(db.Text, unique = False)
   projects = db.relationship('Project')
   


