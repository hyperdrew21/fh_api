from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'FH_api.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)




## user model and crud operations ##
class User(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(75), unique=True)
    password = db.Column(db.String(25), unique=True)
    name = db.Column(db.String(75), unique=False)
    streetAddress1 = db.Column(db.String(100), unique=False)
    streetAddress2 = db.Column(db.String(100), unique=False)
    city = db.Column(db.String(40), unique=False)
    state = db.Column(db.String(2), unique=False)
    zipcode = db.Column(db.String(5), unique=False)
    
    def __init__(self, email, password, name, streetAddress1, streetAddress2, city, state, zipcode):
        self.email = email
        self.password = password
        self.name = name
        self.streetAddress1 = streetAddress1
        self.streetAddress2 = streetAddress2
        self.city = city
        self.state = state
        self.zipcode = zipcode
    
class UserSchema(ma.Schema):
    class Meta: 
        fields = ('id', 'email', 'password', 'name', 'streetAddress1', 'streetAddress2', 'city', 'state', 'zipcode')
            
user_schema = UserSchema()
users_schema = UserSchema(many=True)
    
@app.route('/user', methods=["POST"])
def add_user(): 
    email = request.json['email']
    password = request.json['password']
    name = request.json['name']
    streetAddress1 = request.json['streetAddress1']
    streetAddress2 = request.json['streetAddress2']
    city = request.json['city']
    state = request.json['state']
    zipcode = request.json['zipcode']
        
    new_user = User(email, password, name, streetAddress1, streetAddress2, city, state, zipcode)
        
    db.session.add(new_user)
    db.session.commit()
        
    user = User.query.get(new_user.id)
        
    return user_schema.jsonify(user)

@app.route("/users", methods=["GET"])
def get_users(): 
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result)

@app.route("/userpass/<id>", methods=["PUT"])
def up_pass(id):
    user = User.query.get(id)
    
    password = request.json['password']
    
    user.password = password
    
    db.session.commit()
    return "Successfully updated password!"

@app.route("/userinfo/<id>", methods=["PUT"])
def user_info(id):
    user = User.query.get(id)
    
    email = request.json['email']
    name = request.json['name']
    streetAddress1 = request.json['streetAddress1']
    streetAddress2 = request.json['streetAddress2']
    city = request.json['city']
    state = request.json['state'] 
    zipcode = request.json['zipcode']   
    
    user.email = "email"
    user.name = "name"
    user.streetAddress1 = "streetAddress1"
    user.streetAddress2 = "streetAddress2"
    user.city = "city"
    user.state = "state"
    user.zipcode = "zipcode"
    
    db.session.commit()
    
    return "Updated info success"

if __name__ == '__main__': 
    app.run(debug=True)
    
    