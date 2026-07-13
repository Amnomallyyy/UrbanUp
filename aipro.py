from flask import Flask,render_template,request,redirect,url_for,jsonify, session, make_response, Blueprint
import json
from intai import run_audit,validate_structures,chat_bot, compute_metrics
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import Flask, request, render_template
from flask_cors import CORS
import json
from transformers import AutoModelForCausalLM, AutoTokenizer


from flask import request, jsonify, session 
Ai = Blueprint('Ai',__name__)
@Ai.route("/chat", methods=["POST"])
def chatAI():
    data = request.get_json() or {}
    user_message = data.get("message", "")
    current_id = None

    if current_id is None:
        response = chat_bot(user_message)
    else:
        response = chat_bot(user_message, interaction_id=current_id)
   
   
   
    reply = response.get("text_reply", "Error: No reply generated.")
    new_id = response.get("new_interaction_id")

    
    if new_id:
        session["interaction_id"] = new_id

    return jsonify({"reply": reply})



@Ai.route("/auditAI", methods=["POST"])
def auditAI():
    data = request.get_json() or {}
    
   
    map_data = data.get('message', [])
    objectives = data.get('objectives', "").strip()
    
    
    if not map_data:
        return jsonify({'reply': 'Audit Hub: No map nodes were received to analyze.'}), 400
        
    try:
       
       reply= json.loads(run_audit(objectives, map_data))
       

       return jsonify({"reply":reply})
    except Exception as e:
        print(f"Backend Audit Crash Details: {e}")
        return jsonify({'reply': 'The AI Audit engine encountered an unexpected error parsing the blueprint.'}), 500
          







