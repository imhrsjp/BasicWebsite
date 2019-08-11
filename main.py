from flask import Flask , render_template ,request
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import json
from datetime import datetime

with open('config.json','r') as c:
    params=json.load(c)['params']

local_server = 'True'
app = Flask(__name__)
if(local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']
db = SQLAlchemy(app)

class Contacts(db.Model):
    eno = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)
    email = db.Column(db.String, nullable=False)
    phone_no = db.Column(db.Integer, nullable=False)
    message = db.Column(db.String, nullable=False)
    date = db.Column(db.String, nullable=True)




@app.route("/")
def home():
    return render_template("index.html",params=params)

@app.route("/about")
def about():
    return render_template("about.html",params=params)

@app.route("/contact" , methods=['GET','POST'])
def contact():
    if (request.method=='POST'):
        eno2 = request.form['eno1']
        name2 = request.form['name1']
        email2 = request.form['email1']
        phone_no2 = request.form['phone_no1']
        message2 = request.form['message1']
        dt = datetime.now()
        entry = Contacts(eno=eno2,name=name2,email=email2,phone_no=phone_no2,message=message2,date=dt)
        db.session.add(entry)
        db.session.commit()
    return render_template("contact.html",params=params)

@app.route("/post")
def post():
    return render_template("post.html",params=params)

@app.route("/login")
def login():
    return render_template("login.html",params=params)

@app.route("/addPost")
def addPost():
    return render_template("addPost.html",params=params)


@app.route("/dashboard",methods=['POST'])
def dashboard():
    if(request.method=='POST'):
        uname = request.form['username']
        password = request.form['pass']
        if(uname==params['username'] and password==params['password']):
            return render_template("dashboard.html",params=params)
        else:
            return render_template("login.html")


if __name__ == '__main__':
    app.run(debug=True)