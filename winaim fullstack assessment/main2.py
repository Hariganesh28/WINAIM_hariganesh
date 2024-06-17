from flask import Flask, request, jsonify,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# Initialize app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    contact = db.Column(db.String(100))

    def __init__(self, name, contact):
        self.name = name
        self.contact = contact

# Schema
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'contact')

# Initialize schema
users_schema = UserSchema(many=True)
user_schema = UserSchema()

# Rest of your Flask app code
@app.route('/')
def home():
   return render_template('index.html')

@app.route('/hari')
def house():
   return render_template('hi.html')


if __name__ == '__main__':
    app.run(debug=True)
