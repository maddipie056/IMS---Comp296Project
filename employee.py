from operator import or_

from flask import Blueprint, render_template, session, redirect, url_for, request
from app import db
from models import Item
from resources.items import Items

employee = Blueprint('employee', __name__, url_prefix='/employee')

@employee.route('/dashboard')
def dashboard():
    if 'loggedin' not in session or session.get('role') != 'employee':
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
        query = query.filter(Item.category==category_filter)
    
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

    raw_categories = db.session.query(Item.category).distinct().all()
    categories = [c[0] for c in raw_categories]

    return render_template('employee/dashboard.html',
                            username=session['username'],
                              total_products=total_products,
                              total_stock=total_stock,
                              out_of_stock=out_of_stock,
                              items = items, 
                              categories = categories)
@employee.route('/products')
def products():
    if 'loggedin' not in session or session.get('role') != 'employee':
        return redirect(url_for('auth.login'))
    search = request.args.get('search', '')
    sort = request.args.get('sort', '')
    category_filter = request.args.get('filter', '')

    print("DEBUG search:", search)
    print("DEBUG sort:", sort)
    print("DEBUG filter:", category_filter)

    query = Item.query
    if search:
        query = query.filter(or_(Item.item_name.ilike(f"{search}%"), Item.item_name.ilike(f"%{search}%")))

    if category_filter:
        query = query.filter(Item.category==category_filter)
    
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

    raw_categories = db.session.query(Item.category).distinct().all()
    categories = [c[0] for c in raw_categories]
    
    return render_template('employee/products.html'
                            , username=session['username']
                           , items=items
                           , categories=categories)
@employee.route('/categories')
def categories():
    if 'loggedin' not in session or session.get('role') != 'employee':
        return redirect(url_for('auth.login'))
    
    items = Item.query.all()
    category_map = {}
    for item in items:
        if item.category not in category_map:
            category_map[item.category] = 0
        category_map[item.category] += 1

    category_counts = db.session.query(Item.category, db.func.count(Item.item_id)).group_by(Item.category).all()

    return render_template('employee/categories.html'
                            , username=session['username']
                           , items=Item.query.all(),
                           category_counts=category_counts)
