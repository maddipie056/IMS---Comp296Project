from flask import Blueprint, render_template, session, redirect, url_for

admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.route('/dashboard')
def dashboard():
    if 'loggedin' not in session or session.get('role') != 'admin':
        return redirect(url_for('auth.login'))
    return render_template('admin/dashboard.html', username=session['username'])

@admin.route('/view_accounts')
def view_accounts():
    if 'loggedin' not in session or session.get('role') != 'admin':
        return redirect(url_for('auth.login'))
    return render_template('admin/view_accounts.html', username=session['username'])

@admin.route('/create_account')
def create_account():
    if 'loggedin' not in session or session.get('role') != 'admin':
        return redirect(url_for('auth.login'))
    return render_template('admin/create_account.html', username=session['username'])

@admin.route('/roles')
def roles():
    if 'loggedin' not in session or session.get('role') != 'admin':
        return redirect(url_for('auth.login'))
    return render_template('admin/roles.html', username=session['username'])
