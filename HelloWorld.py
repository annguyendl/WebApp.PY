import uuid, os
import pandas
from flask import Flask, render_template, request, send_file
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
from send_email import send_email
from sqlalchemy.sql import func
from werkzeug.utils import secure_filename
import geopy.geocoders
from geopy.geocoders import Nominatim
import certifi
import ssl

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
    global filename
    if request.method=='POST':        
        upload_file = request.files["upload_file"]
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, 'static/uploadimg/' + str(uuid.uuid4().hex) + "." + upload_file.filename.split(".")[-1])
        upload_file.save(filename)
        #TODO: Save the file path, original filename to database

    #TODO: build the uploaded file list from database to display in 'download.html'
    return render_template("success.html",
    msg='Images are uploaded successful to [%s].' % (filename), btn="download.html")

@app.route('/upcontactfile', methods=['POST'])
def upcontactfile():
    global filename
    if request.method=='POST':        
        upload_file = request.files["upload_file"]
        try:
            df = pandas.read_csv(upload_file)
            ctx = ssl.create_default_context(cafile=certifi.where())
            geopy.geocoders.options.default_ssl_context = ctx

            gc = Nominatim(user_agent="Flask-WebApp", scheme='http')
            df["coordinates"] = df["Address"].apply(gc.geocode)
            df["Latitude"] = df["coordinates"].apply(lambda x: x.latitude if x != None else None)
            df["Longitude"] = df["coordinates"].apply(lambda x: x.longitude if x != None else None)            
            df = df.drop("coordinates", 1)

            dirname = os.path.dirname(__file__)
            filename = os.path.join(dirname, 'static/uploadcsv/' + str(uuid.uuid4().hex) + "." + upload_file.filename.split(".")[-1])
            df.to_csv(filename, index=None)

            return render_template("success.html",
            msg='File is uploaded successful. Due to .' % (filename), btn="download.html",
            text=df.to_html())
        except Exception as e:
            return render_template("contact.html",
            errmsg="Error: " + str(e))

@app.route('/download')
def download():
    # smile = "Take_a_smile.jpg"
    # dirname = os.path.dirname(__file__)
    # filename = os.path.join(dirname, 'static/uploadimg/' + smile)
    return send_file(filename, attachment_filename=filename.split("/")[-1], as_attachment=True)

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/projects')
def projects():
    return render_template("projects.html")

@app.route('/datacollection')
def datacollection():
    return render_template("collectingdata.html")

@app.route('/tech')
def tech():
    import datetime
    from pandas_datareader import data
    from bokeh.plotting import figure, show, output_file
    from bokeh.embed import components
    from bokeh.resources import CDN

    def dec_inc(close_price, open_price):
        if close_price > open_price:
            return "Increase"
        elif close_price < open_price:
            return "Decrease"
        else:
            return "Equal"

    startdt = datetime.datetime(2021, 1, 1)
    enddt = datetime.datetime(2021, 10, 23)
    df = data.DataReader(name="AAPL", data_source="yahoo", start=startdt, end=enddt)

    p=figure(x_axis_type='datetime', width=1000, height=300, sizing_mode="scale_width")
    p.title="Candlestick chart"

    p.grid.grid_line_alpha=0.3

    p.segment(df.index, df.High, df.index, df.Low, color="Black")

    df["Status"]=[dec_inc(c, o) for c, o in zip(df.Close, df.Open)]

    df["Middle"]=(df.Open+df.Close)/2

    df["Diff"]=abs(df.Open-df.Close)

    hour_12=12*60*60*1000
    p.rect(df.index[df.Status=="Increase"], df.Middle[df.Status=="Increase"], hour_12, df.Diff[df.Status=="Increase"], fill_color="green", line_color="black")
    p.rect(df.index[df.Status=="Decrease"], df.Middle[df.Status=="Decrease"], hour_12, df.Diff[df.Status=="Decrease"], fill_color="red", line_color="black")

    script1, div1 = components(p)
    cdn_js = CDN.js_files
    cdn_css = CDN.css_files

    return render_template("tech.html", script1=script1, div1=div1, cdn_js1=cdn_js[0])

if __name__=="__main__":
    app.run(debug=True)
