from flask import *  
import pandas as pd
import csv
import base64
from flask_pymongo import PyMongo



app = Flask(__name__) 
# mongoDB configuration
app.config["MONGO_URI"]="mongodb+srv://hari:12345@cluster0.avyit.mongodb.net/csvfile?retryWrites=true&w=majority"
mongo =PyMongo(app) 
db=mongo.db
logindetails=db.logindetails
filemanager =db.filemanager

# login page...
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    global emailId
    emailId = request.form['emailId']
    passwd = request.form['passwd']

    userFound =logindetails.find_one({
        "emailId" : emailId,
        "password"  : passwd
    })
    
    if not userFound:
        return jsonify({"response":"0"})
    else:
        return jsonify({"response" : "1"})

# create admin account....
@app.route('/create', methods=["GET"])
def createaccount():
    return render_template("create.html")
@app.route('/updatedetails', methods=['POST'])
def updatedetails():
    emailId = request.form['createEmailId']
    userName = request.form['userName']
    passwd = request.form['createPasswd']
    
    checkEmailExists = logindetails.find_one({'emailId' : emailId})
    checkNameExists = logindetails.find_one({'username' : userName})
    if checkEmailExists:
        return jsonify({'response' : '0'})
    elif checkNameExists:
        return jsonify({'response' : '1'})
    else:
        accountDetails = {
            'emailId'    : emailId,
            'username'   : userName,
            'password'   : passwd
        }
        insert =logindetails.insert_one(accountDetails)
        return jsonify({'response' : '2'})

@app.route('/upload')  
def upload():  
    return render_template("upload.html")  
 
@app.route('/success', methods = ['POST'])  
def success():  
    check = logindetails.find_one({'emailId' : emailId})
    username=check['username']
    fileData =db[username]  
    f = request.files['file']  
    f.save(f.filename)  
    csvfile = open(f.filename)
    reader = csv.DictReader( csvfile )
    reader=list(reader)
    length=len(reader)
    header= reader[0]
    have=0
    for each in reader:
        row={}
        for field in header:
            if(field.lower()=='password'):
                have=1
                password = each[field].encode("utf-8")
                encoded = base64.b64encode(password)
                #print(encoded)
                row[field]=encoded
            else:
                row[field]=each[field]
        insert =fileData.insert_one(row)
    if(have==1):
        passwo="Password column found ,encode and store in database"
    elif(have==0):
        passwo="Password column not found "

    return render_template("success.html",message="File uploaded successfully",length=length,passwo=passwo) 
        
    
  
if __name__ == '__main__':  
    app.run(debug = True)  