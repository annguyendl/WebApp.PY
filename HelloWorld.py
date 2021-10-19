from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
from send_email import send_email
from sqlalchemy.sql import func

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://bookinv:%s@localhost/bookinv' % quote('bookinv@12345')
db=SQLAlchemy(app)

class Data(db.Model):
    __tablename__="data"
    id=db.Column(db.Integer, primary_key=True)
    email_=db.Column(db.String(120), unique=True)
    height_=db.Column(db.Integer)

    def __init__(self, email_, height_):
        self.email_=email_
        self.height_=height_


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/about', methods=['POST', 'GET'])
def about():
    return render_template("about.html")

@app.route('/success', methods=['POST'])
def success():
    if request.method=='POST':
        email = request.form['email_name']
        height = request.form['height_name']
        print(email, height)
        if db.session.query(Data).filter(Data.email_==email).count() == 0:
            dat=Data(email_=email, height_=height)
            db.session.add(dat)
            db.session.commit()
            avg_height = db.session.query(func.avg(Data.height_)).scalar()
            cnt_height = db.session.query(Data.height_).count()
            send_email(email, height, avg_height, cnt_height)
            return render_template("success.html")
    return render_template("collectingdata.html",
    errmsg='You already got the analysis result for this email address. Please try the new one.')

@app.route('/contact/')
def contact():
    return render_template("contact.html")

@app.route('/tech/')
def tech():
    return render_template("tech.html")

@app.route('/projects/')
def projects():
    return render_template("projects.html")

@app.route('/datacollection/')
def datacollection():
    return render_template("collectingdata.html")

if __name__=="__main__":
    app.run(debug=True)
