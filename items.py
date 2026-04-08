from flask_restful import Resource, reqparse
from application import db
from models import Item

item_args = reqparse.RequestParser()
item_args.add_argument('item_name', type=str, required=True, help="Item name is required")
item_args.add_argument('category', type=str)
item_args.add_argument('sku', type=str)
item_args.add_argument('quantity', type=int, required=True, help="Item name is required")
item_args.add_argument('low_stock_threshold', type=int)


class Items(Resource):
    def get(self, item_id=None):
        if item_id:
            item = Item.query.get_or_404(item_id)
            return {col: getattr(item, col) for col in item.__table__.columns.keys()}
        items = Item.query.all()
        return [{col: getattr(i, col) for col in i.__table__columns.key()} for i in items]
    def post(self):
        args = item_args.parse_args()
        item = Item(**args)
        db.session.add(item)
        db.session.commit()
        return {"message": "Item created"},201
    
    def put(self,item_id):
        item = Item.query.get_or_404(item_id)
        args = item_args.parse_args()
        for key, value in args.items():
            setattr(item, key, value)
        db.session.commit()
        return {"message": "Item updated"}
    
    def delete(self, item_id):
        item = Item.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item deleted"}
