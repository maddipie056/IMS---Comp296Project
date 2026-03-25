from flask import Blueprint, render_template, session, redirect, url_for

admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.route('/dashboard')
def dashboard():
    if 'loggedin' not in session or session.get('role') != 'admin':
        return redirect(url_for('auth.login'))
    return render_template('admin/dashboard.html', username=session['username'])