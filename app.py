from flask import Flask,render_template,request,redirect,url_for
import json

app = Flask(__name__, template_folder= "templates")
#Flask() is a class that deaks wuth communicating with the 
#web browser
@app.route('/', methods = ['GET','POST'])
def  mainPage():
   #if submit 
     #arrayList = request.json.get(arrayList)
     #if arrayList is None:
        # pass
         #Try again
   if request.method == "POST":
      user = request.form["nm"]
      if user == "Amna":
          return "success"
      else: return "Failure"
   elif request.method == "GET":
      return render_template("index.html")
     #request.json gets you a dicitionary
     #get, means get the specifific ellemnt
@app.route("/<usr>")
def user(usr):
   return f"<h1>{usr}</h1>"

@app.route('/file_upload', methods = ["GET","POST"])
def file_upload():
   if request.method == "POST":
       file = request.files["json_file"]

       if file.content_type =='application/json':
         filebytes = file.read()
         
         return json.loads(filebytes)
       else:
         return "failure"
if __name__ == '__main__':
   app.run(host = '0.0.0.0',debug = True)

 