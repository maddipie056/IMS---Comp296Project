from flask import Flask, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
import os
from resources.items import Items, ItemLookup



db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:SgOvpW22*!@localhost/inventorymgmtsys'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = os.urandom(30)
    
    db.init_app(app)

    
    with app.app_context():
        db.Model.metadata.reflect(bind=db.engine)

    from apps.auth import auth
    app.register_blueprint(auth)

    from apps.admin import admin
    from apps.manager import manager
    from apps.employee import employee

    app.register_blueprint(admin)
    app.register_blueprint(manager)
    app.register_blueprint(employee)

    api = Api(app)

    from resources.items import Items
    from resources.staff import Staff
    from resources.adjustments import StockAdjustmentAPI

    api.add_resource(Items,'/api/items/<int:item_id>')
    api.add_resource(Staff,'/api/staff/<int:staff_id>')
    api.add_resource(StockAdjustmentAPI,'/api/adjustments','/api/adjustments/<int:adjustment_id>')
    api.add_resource(ItemLookup,'/api/items/lookup')



    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))


    return app
