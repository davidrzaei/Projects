from flask import Flask, flash, render_template, request, jsonify, redirect, url_for, session, g
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

migrate = Migrate(app, db)

# Define your models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    todos = db.relationship('Todo', backref='user', lazy=True)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@app.before_request
def before_request():
    g.user = None
    if 'username' in session:
        g.user = User.query.filter_by(username=session['username']).first()

    # Redirect to login if user is not logged in and trying to access a protected route
    if not g.user and request.endpoint not in ['login', 'register']:
        return redirect(url_for('login'))

@app.route('/')
def index():
    if g.user:
        todos = Todo.query.filter_by(user_id=g.user.id).all()
    else:
        todos = []
    return render_template('index.html', todos=todos)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['username'] = username  # Store username in session
            flash('Logged in successfully!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login unsuccessful. Please check your username and password.', 'error')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if User.query.filter_by(username=username).first():
            return render_template('error.html', error='Username already exists')
        elif password != confirm_password:
            return render_template('error.html', error='Password and Confirm Password do not match')

        new_user = User(username=username, password=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()
        session['username'] = username
        return redirect(url_for('index'))

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)  # Clear the session
    flash('Logged out successfully!', 'success')
    return redirect(url_for('login'))

@app.route('/add', methods=['POST'])
def add_todo():
    content = request.form['content']
    new_todo = Todo(content=content, user_id=g.user.id)
    db.session.add(new_todo)
    db.session.commit()
    flash('Todo added successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/delete/<int:id>', methods=['POST'])
def delete_todo(id):
    todo_to_delete = Todo.query.get_or_404(id)
    if todo_to_delete.user_id == g.user.id:
        db.session.delete(todo_to_delete)
        db.session.commit()
        flash('Todo deleted successfully!', 'success')
    else:
        flash('Unauthorized to delete this todo!', 'error')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
