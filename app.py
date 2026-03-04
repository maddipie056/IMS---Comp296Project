from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
import os



db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:SgOvpW22*!@localhost/inventorymgmtsys'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = os.urandom(30)
    
    db.init_app(app)

    
    with app.app_context():
        db.Model.metadata.reflect(bind=db.engine)

    from auth import auth
    app.register_blueprint(auth)

    api = Api(app)

    from resources.items import Items
    from resources.staff import Staff
    from resources.adjustments import StockAdjustment

    api.add_resource(Items,'/api/items/<int:item_id>')
    api.add_resource(Staff,'/api/staff/<int:staff_id>')
    api.add_resource(StockAdjustment,'/api/adjustments/<int:adjustment_id>')


    
    @app.route('/')
    def home():
        return redirect(url_for('auth.login'))

    return app
