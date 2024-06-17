from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from functools import wraps
from datetime import date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hrms.db'
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    employees = db.relationship('Employee', backref='department', lazy=True)

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    employees = db.relationship('Employee', backref='role', lazy=True)

class PerformanceReview(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    review_date = db.Column(db.Date, nullable=False)
    comments = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False)

def role_required(role):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            identity = get_jwt_identity()
            if identity['role'] != role:
                return jsonify({'message': 'Access denied'}), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper

@app.route('/register', methods=['POST'])
def register_post():
    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(username=data['username'], password=hashed_password, role=data['role'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered'}), 201

@app.route('/login', methods=['POST'])
def login_post():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if not user or not bcrypt.check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Invalid credentials'}), 401
    access_token = create_access_token(identity={'username': user.username, 'role': user.role})
    return jsonify({'access_token': access_token}), 200

@app.route('/employees', methods=['POST'])
@jwt_required()
@role_required('HR')
def create_employee():
    data = request.get_json()
    new_employee = Employee(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        department_id=data['department_id'],
        role_id=data['role_id']
    )
    db.session.add(new_employee)
    db.session.commit()
    return jsonify({'message': 'Employee created'}), 201

@app.route('/employees/<int:id>', methods=['PUT'])
@jwt_required()
@role_required('HR')
def update_employee(id):
    data = request.get_json()
    employee = Employee.query.get(id)
    if not employee:
        return jsonify({'message': 'Employee not found'}), 404
    employee.first_name = data['first_name']
    employee.last_name = data['last_name']
    employee.email = data['email']
    employee.department_id = data['department_id']
    employee.role_id = data['role_id']
    db.session.commit()
    return jsonify({'message': 'Employee updated'}), 200

@app.route('/employees/<int:id>', methods=['DELETE'])
@jwt_required()
@role_required('HR')
def delete_employee(id):
    employee = Employee.query.get(id)
    if not employee:
        return jsonify({'message': 'Employee not found'}), 404
    db.session.delete(employee)
    db.session.commit()
    return jsonify({'message': 'Employee deleted'}), 200

@app.route('/employees/<int:id>', methods=['GET'])
@jwt_required()
def get_employee(id):
    employee = Employee.query.get(id)
    if not employee:
        return jsonify({'message': 'Employee not found'}), 404
    return jsonify({
        'first_name': employee.first_name,
        'last_name': employee.last_name,
        'email': employee.email,
        'department': employee.department.name if employee.department else None,
        'role': employee.role.name if employee.role else None
    }), 200

@app.route('/departments', methods=['POST'])
@jwt_required()
@role_required('HR')
def create_department():
    data = request.get_json()
    new_department = Department(name=data['name'])
    db.session.add(new_department)
    db.session.commit()
    return jsonify({'message': 'Department created'}), 201

@app.route('/roles', methods=['POST'])
@jwt_required()
@role_required('HR')
def create_role():
    data = request.get_json()
    new_role = Role(name=data['name'])
    db.session.add(new_role)
    db.session.commit()
    return jsonify({'message': 'Role created'}), 201

@app.route('/performance_reviews', methods=['POST'])
@jwt_required()
@role_required('HR')
def create_performance_review():
    data = request.get_json()
    new_review = PerformanceReview(
        employee_id=data['employee_id'],
        review_date=date.fromisoformat(data['review_date']),
        comments=data['comments'],
        rating=data['rating']
    )
    db.session.add(new_review)
    db.session.commit()
    return jsonify({'message': 'Performance review created'}), 201

@app.route('/performance_reviews/<int:id>', methods=['PUT'])
@jwt_required()
@role_required('HR')
def update_performance_review(id):
    data = request.get_json()
    review = PerformanceReview.query.get(id)
    if not review:
        return jsonify({'message': 'Performance review not found'}), 404
    review.review_date = date.fromisoformat(data['review_date'])
    review.comments = data['comments']
    review.rating = data['rating']
    db.session.commit()
    return jsonify({'message': 'Performance review updated'}), 200

@app.route('/performance_reviews/<int:id>', methods=['DELETE'])
@jwt_required()
@role_required('HR')
def delete_performance_review(id):
    review = PerformanceReview.query.get(id)
    if not review:
        return jsonify({'message': 'Performance review not found'}), 404
    db.session.delete(review)
    db.session.commit()
    return jsonify({'message': 'Performance review deleted'}), 200

@app.route('/performance_reviews/<int:id>', methods=['GET'])
@jwt_required()
def get_performance_review(id):
    review = PerformanceReview.query.get(id)
    if not review:
        return jsonify({'message': 'Performance review not found'}), 404
    return jsonify({
        'employee_id': review.employee_id,
        'review_date': review.review_date.isoformat(),
        'comments': review.comments,
        'rating': review.rating
    }), 200

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login',methods=['GET'])
def login():
    return render_template('login.html')

@app.route('/register',methods=['GET'])
def register():
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
