from flask import Flask, request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
import hashlib

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Using MD5 for hashing (not recommended for production)
        password_hash = hashlib.md5(password.encode()).hexdigest()
        
        new_user = User(username=username, password_hash=password_hash)
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Hash the provided password for comparison
        password_hash = hashlib.md5(password.encode()).hexdigest()
        
        user = User.query.filter_by(username=username, password_hash=password_hash).first()
        
        if user:
            return redirect(url_for('dashboard'))
        else:
            return 'Login Failed'
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return 'Welcome to your dashboard'

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)