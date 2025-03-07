from flask import render_template, Blueprint, request, redirect, url_for, flash, session, g
from .models import User, Todo

bp = Blueprint('main', __name__)

@bp.before_request
def before_request():
    g.user = None
    if 'username' in session:
        g.user = User.query.filter_by(username=session['username']).first()

@bp.route('/')
def index():
    if g.user:
        user_todos = Todo.query.filter_by(user_id=g.user.id).all()
    else:
        user_todos = []
    return render_template('index.html', todos=user_todos)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['username'] = username
            flash('Logged in successfully!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login unsuccessful. Please check your username and password.', 'error')
    return render_template('login.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if User.query.filter_by(username=username).first():
            return render_template('error.html', error='Username already exists')
        elif password != confirm_password:
            return render_template('error.html', error='Password and Confirm Password do not match')
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        session['username'] = username
        flash('Registered and logged in successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('register.html')

@bp.route('/logout')
def logout():
    session.pop('username', None)
    flash('Logged out successfully!', 'success')
    return redirect(url_for('login'))

@bp.route('/add', methods=['POST'])
def add_todo():
    content = request.form['content']
    new_todo = Todo(content=content, user_id=g.user.id)
    db.session.add(new_todo)
    db.session.commit()
    flash('Todo added successfully!', 'success')
    return redirect(url_for('index'))

@bp.route('/delete/<int:id>', methods=['POST'])
def delete_todo(id):
    todo = Todo.query.get(id)
    if todo and todo.user_id == g.user.id:
        db.session.delete(todo)
        db.session.commit()
        flash('Todo deleted successfully!', 'success')
    return redirect(url_for('index'))
