from flask import Flask,render_template,request,redirect,url_for,jsonify, session, make_response,flash
import json
#from intai import run_audit,validate_structures, parse_audit_for_chatbot,calculate_spatial_metrics,chat_bot
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import Blueprint, render_template, request
from models import Project, User
from auth import auth
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user,login_required, logout_user,current_user
from Final import db
Proj = Blueprint('Proj',__name__)
   
@Proj.route('/createFile', methods = ['GET','POST'])
def saveFiles():
        if request.method == "POST":
            filename = request.form.get('filename'),
            aiAdvice = session["aiAdvice"],
            jsonMapData = request.json.get()
            project = Project(
                fileName = filename,
                aiAdvice = aiAdvice,
                jsonMapData = jsonMapData)
            db.session.add(project,user_id = 'user.id')
            db.session.commit()
            redirect(url_for('Proj.SavedFiles', filename = filename))
        return render_template("savedfiles.html", user = current_user)



@Proj.route("/SavedFiles/<string:filename>")
def project_details(filename):
    files = db.get_or_404(Project,filename).first()

    
    json_data =  files.json_data
    ai_advice = files.ad_advice

    return render_template(
        "da.html", 
        filename=filename, 
        project_data=json_data, 
        ai_advice=ai_advice
    )
  
   

@Proj.route("/SavedFiles/<filename>/delete", methods =["GET","POST"])
def project_Delete(filename):
        project  = db.get_or_404("POST")
        if request.method == "POST":
            db.session.delete(project)
            db.sesssion.commit()
            return render_template('savedfiles')
        
   


