from flask import Flask, render_template, request, redirect, url_for, jsonify, session, make_response
import json
#from intai import run_audit, validate_structures, parse_audit_for_chatbot, calculate_spatial_metrics, chat_bot
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, template_folder="templates")
   
    app.secret_key = 'hhkhjhihuhuhihj'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./site.db'
   
    db.init_app(app)
    from models import User, Project
    from auth import auth
    from projectblueprint import Proj
    from aipro import Ai
    

    with app.app_context():
        db.create_all()


    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(Proj, url_prefix='/')
    app.register_blueprint(Ai, url_prefix='/')

    migrate = Migrate(app, db)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app