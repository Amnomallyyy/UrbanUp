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
   
@Proj.route("/createProj", methods = ['GET','POST'])
def saveFiles():
    if request.method == "POST":
      
        raw_payload = request.form.get('project_payload')
        
        
        if raw_payload:
            data = json.loads(raw_payload)
        else:
            data = {}

      
        filename = data.get('filename', "")
        aiAdvice = data.get('aiadvice', "")
        jsonMapData = data.get('jsonmapdata', [])
        
        
        project = Project(
            fileName=filename,
            aiAdvice=aiAdvice,
            jsonMapData=json.dumps(jsonMapData),
            user_id=current_user.id
        )
        db.session.add(project)
        db.session.commit()
        
        
        return render_template("savedfiles.html", user=current_user)
    return render_template('working.html')

    
        




@Proj.route("/SavedFiles/<string:filename>/<int:id>")
def project_details(filename, id):
    
    files = db.get_or_404(Project, id) 

   
    try:
        json_data = json.loads(files.jsonMapData)
    except:
      
        json_data = [] 

    ai_advice = files.aiAdvice

    return render_template(
        "da.html", 
        filename=filename,
        id=id,
        project_data=json_data, 
        ai_advice=ai_advice
    )


@Proj.route("/SavedFiles/<int:id>/delete", methods=["POST"])
def project_Delete(id):
    
    
    project = db.get_or_404(Project, id)
    
    db.session.delete(project)
    db.session.commit()
    
    return redirect(url_for('Proj.SavedFiles'))
   


