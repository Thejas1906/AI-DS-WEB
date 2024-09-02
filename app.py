from flask import Flask
from flask import render_template,request,redirect,session
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session

app = Flask(__name__, static_url_path='/static')

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://yogi:passwd@localhost/todo"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the model
class Datas(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    mobilenumber = db.Column(db.String(15), unique=True, nullable=False)
    college = db.Column(db.String(100), nullable=False)
    teamname = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<data {self.name}>'

# Create the database and tables
with app.app_context():
    db.create_all()


@app.route('/store_data', methods=['POST'])
def strore_data():
    name = request.form['name']
    mobilenumber = request.form['mobilenumber']
    college = request.form['college']
    teamname = request.form['teamname']
    
    data = Datas(
        name=name,
        mobilenumber=mobilenumber,
        college=college,
        teamname=teamname
    )
    
    db.session.add(data)
    db.session.commit()
    
    return 'Data added successfully!'

@app.route('/datas')
def datas():
    all_datas = Datas.query.all()
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

if __name__ == '__main__':
    app.run(debug=True)