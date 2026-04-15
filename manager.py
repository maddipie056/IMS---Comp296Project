from flask import Blueprint, current_app, render_template, session, redirect, url_for, request
from sqlalchemy import or_
from apps import db 
from apps.models import Category, Item
from resources import items


manager = Blueprint('manager', __name__, url_prefix='/manager')

@manager.route('/dashboard')
def dashboard():
    if 'loggedin' not in session or session.get('role') != 'manager':
        return redirect(url_for('auth.login'))
    
    search = request.args.get('search', '')
    sort = request.args.get('sort', '')
    category_filter = request.args.get('filter', '')


    query = Item.query
    if search:
        query = query.filter(or_(Item.item_name.ilike(f"{search}%"), Item.item_name.ilike(f"%{search}%")))

    if category_filter:
        query = query.filter(Item.category_id==int(category_filter))
    
    if sort == 'name_asc':
        query = query.order_by(Item.item_name.asc())
    elif sort == 'name_desc':
        query = query.order_by(Item.item_name.desc())
    elif sort == 'quantity_asc':
        query = query.order_by(Item.quantity.asc())
    elif sort == 'quantity_desc':
        query = query.order_by(Item.quantity.desc())

    items = query.all()

    total_products = len(items)
    total_stock = sum(item.quantity for item in items)
    out_of_stock = sum(1 for item in items if item.quantity == 0)

    low_stock_items = [item for item in items if item.quantity < item.low_stock_threshold and item.quantity > 0]

    categories = Category.query.all()

    return render_template('manager/dashboard.html', username=session['username']
                           , items=items,
                           total_products=total_products,
                           total_stock=total_stock,
                           out_of_stock=out_of_stock,
                           categories = categories,
                           low_stock_items=low_stock_items)

@manager.route('/products')
def products():
    if 'loggedin' not in session or session.get('role') != 'manager':
        return redirect(url_for('auth.login'))
    search = request.args.get('search', '')
    sort = request.args.get('sort', '')
    category_filter = request.args.get('filter', '')

    print("DEBUG search:", search)
    print("DEBUG sort:", sort)
    print("DEBUG filter:", category_filter)

    query = Item.query
    if search:
        query = query.filter(Item.item_name.ilike(f'%{search}%'))

    if category_filter:
        query = query.filter(Item.category_id==int(category_filter))
    
    if sort == 'name_asc':
        query = query.order_by(Item.item_name.asc())
    elif sort == 'name_desc':
        query = query.order_by(Item.item_name.desc())
    elif sort == 'quantity_asc':
        query = query.order_by(Item.quantity.asc())
    elif sort == 'quantity_desc':
        query = query.order_by(Item.quantity.desc())

    items = query.all()

    total_products = len(items)
    total_stock = sum(item.quantity for item in items)
    out_of_stock = sum(1 for item in items if item.quantity == 0)

    categories = Category.query.all()

    return render_template('manager/products.html'
                            , username=session['username']
                           , items=items,
                           categories = categories, staff_id=session['staff_id'],  threshold = current_app.config.get('LOW_STOCK_THRESHOLD', 10))

@manager.route('/categories')
def categories():
    if 'loggedin' not in session or session.get('role') != 'manager':
        return redirect(url_for('auth.login'))
    
    items = Item.query.all()
    category_map = {}
    for item in items:
        if item.category not in category_map:
            category_map[item.category] = 0
        category_map[item.category] += 1

    category_counts = db.session.query(Category.name, db.func.count(Item.item_id)).outerjoin(Item, Category.category_id == Item.category_id).group_by(Category.name).all()

    return render_template('manager/categories.html'
                            , username=session['username']
                           , items=Item.query.all(),
                           categories=category_counts)
@manager.route('/low_stock')
def low_stock():
    threshold = current_app.config.get('LOW_STOCK_THRESHOLD', 10)

    low_stock_items = Item.query.filter(Item.quantity < threshold).all()

    return render_template('manager/low_stock.html', username=session['username'], low_stock_items=low_stock_items, threshold=threshold, staff_id=session['staff_id'])
@manager.route('/reports')
def reports():
    return render_template('manager/reports.html', username=session['username'])

@manager.route('/api/update-threshold', methods=['POST'])
def update_threshold():
    if 'loggedin' not in session or session.get('role') != 'manager':
        return redirect(url_for('auth.login'))
    
    new_threshold = request.form.get('threshold')
    if new_threshold is not None:
        try:
            new_threshold = int(new_threshold)
            current_app.config['LOW_STOCK_THRESHOLD'] = new_threshold
            return redirect(url_for('manager.low_stock'))
        except ValueError:
            return "Invalid threshold value", 400
    return "Threshold value is required", 400
