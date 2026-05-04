from flask import Blueprint, render_template, session, redirect, url_for, request
from werkzeug.security import generate_password_hash
from apps.models import StockAdjustment, db, Staff, Role

admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.route('/dashboard')
def dashboard():
    if 'loggedin' not in session or session.get('role') != 'admin':
        return redirect(url_for('auth.login'))
    
    all_accounts = Staff.query.count()
    active_employees = Staff.query.filter_by(role_id=1, is_active=True).count()
    active_managers = Staff.query.filter_by(role_id=2, is_active=True).count()
    inactive_accounts = Staff.query.filter_by(is_active=False).count()

    recent_logs = StockAdjustment.query.order_by(
        StockAdjustment.adjustment_timestamp.desc()).limit(10).all()

    return render_template('admin/dashboard.html', username=session['username'],
                           all_accounts = all_accounts, active_employees = active_employees, 
                           active_managers = active_managers, inactive_accounts = inactive_accounts,
                           recent_logs = recent_logs)


@admin.route('/view_accounts')
def view_accounts():
    if 'loggedin' not in session or session.get('role') != 'admin':
        return redirect(url_for('auth.login'))
    
    search = request.args.get('search', '')
    role = request.args.get('role', '')
    query = Staff.query

    if search:
        query = query.filter(
            (Staff.username.ilike(f"%{search}%")) | 
            (Staff.first_name.ilike(f"%{search}%")) |
            (Staff.last_name.ilike(f"%{search}%"))
        )
    
    if role:
        query = query.filter(Staff.role == role)

    users = query.all()

    return render_template('admin/view_accounts.html', 
                           username=session['username'], users = users,
                           role = role, search = search
                           )



@admin.route('/create_account', methods = ['GET', 'POST'])
def create_account():
    if 'loggedin' not in session or session.get('role') != 'admin':
        return redirect(url_for('auth.login'))
    
    roles = Role.query.all()
    if request.method == 'POST':
        first = request.form['first_name']
        last = request.form['last_name']
        email = request.form['email']
        phone_number = request.form['phone_number']
        username = request.form['username']
        password = request.form['password']
        role_id = int(request.form['role_id'])

        role_name = next(r.name for r in roles if r.id == role_id)

        is_active = True



        if Staff.query.filter_by(username = username).first():
            return redirect(url_for('admin.create_account', error="username"))

        if Staff.query.filter_by(email = email).first():
            return redirect(url_for('admin.create_account', error="email"))
        
        password_hash = generate_password_hash(password)

        new_user = Staff(
            first_name = first,
            last_name = last,
            email = email,
            phone_number = phone_number,
            username = username,
            password_hash = password_hash,
            role = role_name,
            role_id = role_id,
            is_active = is_active,
        )

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('admin.view_accounts', success = "created"))

    return render_template('admin/create_account.html', 
                           username=session['username'], 
                           roles=roles,
                           error=request.args.get("error"))

@admin.route('/deactivate_account/<int:user_id>', methods = ['POST'])
def deactivate_account(user_id):
    if 'loggedin' not in session or session.get('role') != 'admin':
        return redirect(url_for('auth.login'))
    
    user = Staff.query.get(user_id)
    if user:
        user.is_active = False
        db.session.commit()
                
    return redirect(url_for('admin.view_accounts', success="deactivated"))

@admin.route('/roles', methods=['GET', 'POST'])
def roles():
    if 'loggedin' not in session or session.get('role') != 'admin':
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        name = request.form['name']
        description = request.form.get('description', '')

        # Prevent duplicate role names
        if Role.query.filter_by(name=name).first():
            return redirect(url_for('admin.roles', error="duplicate"))

        new_role = Role(name=name, description=description)
        db.session.add(new_role)
        db.session.commit()

        return redirect(url_for('admin.roles', success="created"))

    roles = Role.query.all()

    return render_template(
        'admin/roles.html',
        username=session['username'],
        roles=roles,
        error=request.args.get("error"),
        success=request.args.get("success")
    )
@admin.route('/edit_account/<int:user_id>', methods=['GET', 'POST'])
def edit_account(user_id):
    if 'loggedin' not in session or session.get('role') != 'admin':
        return redirect(url_for('auth.login'))

    user = Staff.query.filter_by(staff_id=user_id).first()
    roles = Role.query.all()

    if not user:
        return redirect(url_for('admin.view_accounts', error="notfound"))

    if request.method == 'POST':
        user.first_name = request.form['first_name']
        user.last_name = request.form['last_name']
        user.email = request.form['email']
        user.phone_number = request.form['phone_number']
        user.username = request.form['username']

        if request.form['password']:
            user.password_hash = request.form['password']


        role_id = int(request.form['role_id'])
        user.role_id = role_id
        user.role = next(r.name for r in roles if r.id == role_id)

        user.is_active = request.form['is_active'] == "1"
        
        db.session.commit()
        return redirect(url_for('admin.view_accounts', success="updated"))

    return render_template('admin/edit_account.html',
                           username=session['username'],
                           user=user,
                           roles = roles)
