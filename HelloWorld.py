from flask import Flask, render_template, request, send_file
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
from send_email import send_email
from sqlalchemy.sql import func
from werkzeug.utils import secure_filename
import uuid, os


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
            
            return render_template("success.html",
            msg="Your data is analyzed successfully. A result was sent to your provided email address. Please check for the analyzed result.")
    
    return render_template("collectingdata.html",
    errmsg='You already got the analysis result for this email address. Please try the new one.')

@app.route('/uploadfile', methods=['POST'])
def uploadfile():
    if request.method=='POST':        
        upload_file = request.files["upload_file"]
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, 'static/uploadimg/' + str(uuid.uuid4().hex) + "." + upload_file.filename.split(".")[-1])
        upload_file.save(filename)
        #TODO: Save the file path, original filename to database

    #TODO: build the uploaded file list from database to display in 'download.html'
    return render_template("success.html",
    msg='Images are uploaded successful to [%s].' % (filename), btn="download.html")

@app.route('/download')
def download():
    smile = "Take_a_smile.jpg"
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'static/uploadimg/' + smile)

    return send_file(filename, attachment_filename="Takeasmile_theyarefree.jpg", as_attachment=True)

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/tech')
def tech():
    return render_template("tech.html")

@app.route('/projects')
def projects():
    return render_template("projects.html")

@app.route('/datacollection')
def datacollection():
    return render_template("collectingdata.html")

if __name__=="__main__":
    app.run(debug=True)
