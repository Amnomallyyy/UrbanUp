from flask import Flask,render_template,request,redirect,url_for,jsonify, session, make_response, Blueprint
import json
from intai import run_audit,validate_structures,chat_bot
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

load_dotenv()


Ai = Blueprint("AI",__name__)
interaction_id = None





@Ai.route("/chat", methods = ["POST"])
def chatAI():
   data = request.get_json()
  
   user_message = data.get("message", "")
  
  
   response =chat_bot(user_message)
   
   reply = response["text_reply"]
   interaction_id = response["new_interaction_id"]
  
   
   return jsonify({"reply": reply})

@Ai.route('/auditAI', methods = ["GET","POST"])
def AuditAI():
   map_data =  request.get_json()
   objectives =  request.get_form()


   if validate_structures(map_data,objectives) == None:
       reply = run_audit(map_data,objectives)
       return jsonify({'reply': reply})

 


   
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
#     try:
#         # Prompt the user for input and save it in the variable 'prompt'
#         prompt = input('You: ')
#         # Use the pipeline to generate a response
#         res = chatbot(prompt, max_length=50)
#         # Print the response from the chatbot
#         print('Chatbot: ' + res[0]['generated_text'])
#     except KeyboardInterrupt:
#         # Exit the loop if the user presses Ctrl+C
#         break        //this is chatot.[y








