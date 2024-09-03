import os
from flask import Flask
from flask import render_template,request,redirect,session
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from sqlalchemy.exc import IntegrityError

app = Flask(__name__, static_url_path='/static')

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the model
class Datas(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    mobilenumber = db.Column(db.String(15), unique=True, nullable=False)
    dept = db.Column(db.String(100), nullable=False)
    college = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    events = db.Column(db.String, nullable=False)
    def __repr__(self):
        return f'<data {self.name}>'

# Create the database and tables
with app.app_context():
    db.create_all()


@app.route('/registering', methods=['POST'])
def store_data():
    name = request.form['name']
    mobilenumber = request.form['mobilenumber']
    dept = request.form['dept']
    college = request.form['college']
    email = request.form['email']
    selected_events = request.form.getlist('events')
    events_str = ','.join(selected_events)

    
    data = Datas(
        name=name,
        mobilenumber=mobilenumber,
        dept=dept,
        college=college,
        email=email,
        events=events_str
    )
    
    try:
        db.session.add(data)
        db.session.commit()
        return render_template('success_redirect.html')
    except IntegrityError:
        db.session.rollback()  # Rollback the session in case of an error
        return render_template('fail_redirect.html')
    
    

@app.route('/datas')
def datas():
    all_datas = Datas.query.all()
    for record in all_datas:
        record.events = record.events.split(',') 
    return render_template('datas.html', datas=all_datas)


@app.route('/technical')
def technical():
    return render_template("technical.html")

@app.route('/non-technical')
def non_technical():
    return render_template("non-technical.html")

@app.route('/register')
def home():
    return render_template("register.html")
