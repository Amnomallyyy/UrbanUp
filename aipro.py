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







# AI.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
# CORS(AI)

# model_name = 
# model = AutoModelForCausalLM.from_pretrained(model_name)
# tokenizer = AutoTokenizer.from_pretrained(model_name)
# conversation_history = []

# @AI.route('/')
# def home():
#     return render_template('index.html')

# @AI.route('/chatbot', methods=['POST'])
# def handle_prompt():
#     data = request.get_data(as_text=True)
#     data = json.loads(data)
#     input_text = data['prompt']
    
#     # Create conversation history string
#     history = "\n".join(conversation_history)
#     # Tokenize the input text and history
#     inputs = tokenizer.encode_plus(history, input_text, return_tensors="pt")
#     # Generate the response from the model
#     outputs = model.generate(**inputs, max_length=100)
#     # Decode the response
#     response = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
    
#     # Add interaction to conversation history
#     conversation_history.append(input_text)
#     conversation_history.append(response)
#     return response


# Make sure to import session at the top of your file!
from flask import request, jsonify, session 

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
   

 


   
   # Step 2: Import libraries and download your model
# From the transformers library, we will use the pipeline class to download our model
# from transformers import pipeline

# # The pipeline class will manage the model for us
# # We will use the 'EleutherAI/gpt-neo-125m' model for this project
# # This will download the model to your local machine (1-2 minutes)
# chatbot = pipeline('text-generation', model='EleutherAI/gpt-neo-125m')

# # Step 3: Create a loop to talk to your chatbot
# # This loop will allow you to have a continuous conversation
# while True:
#     







