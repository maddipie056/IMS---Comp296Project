from flask import render_template, request, redirect, url_for, session
from werkzeug.security import check_password_hash, generate_password_hash
from . import db
from apps.models import Staff
from flask import Blueprint

auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = Staff.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            session['loggedin'] = True
            session['staff_id'] = user.staff_id
            session['username'] = user.username
            session['role'] = user.role
            
            if user.role == 'admin':
                return redirect(url_for('admin.dashboard'))
            elif user.role == 'manager':
                return redirect(url_for('manager.dashboard'))
            else:
                return redirect(url_for('employee.dashboard'))
        else:
            msg = "Incorrect username or password"
            
    return render_template('index.html', msg=msg)
    

@auth.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'role' in request.form:
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        role = request.form['role']

        new_user = Staff(username = username, password_hash=password, role=role)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth.route('/profile')
def profile():
    if 'loggedin' not in session:
        return redirect(url_for('auth.login'))
    user = Staff.query.get(session['staff_id'])
    return render_template('profile.html', user = user)

@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
