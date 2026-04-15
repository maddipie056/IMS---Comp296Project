from flask import Flask, redirect, render_template, url_for
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
import os



db = SQLAlchemy()

def create_app():
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    app = Flask(__name__, template_folder=os.path.join(BASE_DIR, 'templates'), static_folder=os.path.join(BASE_DIR, 'static'))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:SgOvpW22*!@localhost/inventorymgmtsys'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = "supersecretkey"

    db.init_app(app)

    with app.app_context():
        db.engine.connect()
        db.Model.metadata.reflect(bind=db.engine)
        from . import models

        from resources.items import Items, ItemLookup
        from resources.staff import Staff
        from resources.adjustments import StockAdjustmentAPI

        api = Api(app)
        api.add_resource(Items, '/api/items', '/api/items/<int:item_id>')
        api.add_resource(Staff, '/api/staff', '/api/staff/<int:staff_id>')
        api.add_resource(ItemLookup, '/api/items/lookup')
        api.add_resource(StockAdjustmentAPI, '/api/adjustments', '/api/adjustments/<int:adjustment_id>')
        

        from .auth import auth
        from .admin import admin
        from .manager import manager
        from .employee import employee

        app.register_blueprint(auth)
        app.register_blueprint(admin)
        app.register_blueprint(manager)
        app.register_blueprint(employee)

        @app.route('/')
        def home():
            return redirect(url_for('auth.login'))

    return app
