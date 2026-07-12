from flask import Blueprint, render_template, request, flash, redirect, url_for
from models import User, Project
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from Final import db
import json
auth = Blueprint('auth', __name__)

@auth.route('/')
def web():
    return render_template('signup.html')

@auth.route('/view')
def view_layout():
    """Intercepts file download shortcuts and forwards coordinates to index.html"""
    raw_layout_data = request.args.get('layout', '[]')
    
    try:
        parsed_data = json.loads(raw_layout_data)
        if isinstance(parsed_data, dict) and "nodes" in parsed_data:
            nodes_array = parsed_data["nodes"]
        else:
            nodes_array = parsed_data if isinstance(parsed_data, list) else []
    except Exception as e:
        print(f"Error parsing shortcut payload: {e}")
        nodes_array = []
        
    return render_template('index.html', shared_layout=json.dumps(nodes_array)) 

@auth.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        firstname = request.form.get('firstName')
        if email:
             email = email.strip().lower()
        user = User.query.filter_by(email=email).first()
        if user:
            flash("This user already exists", category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(firstname) < 2:
            flash('First name must be greater than 1 characters.', category='error')
        elif password1 != password2:
            flash('Passwords dont match', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            # Note: Make sure "password" is lowercase here if it is lowercase in models.py
            user = User(email=email, firstname=firstname, password=generate_password_hash(password1))
            db.session.add(user)
            db.session.commit()
            flash('Account created!', category='success')
            login_user(user, remember=True)
            return redirect(url_for('auth.login'))
    
   
    return render_template('signup.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')  
        if email:
             email = email.strip().lower()
        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                flash('Logged In Successful', category='success')
                login_user(user, remember=True)
                return redirect(url_for('auth.view_layout'))
            else:
                flash('Incorrect Password, Try again', category='error')
                return "password is incorrect"
        else:
            flash('Email does not Exist', category='error')
            return "email doesnt exist"

  
    return render_template('login.html') 

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))