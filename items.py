from flask_restful import Resource, reqparse
from apps import db
from apps.models import Item, Category

item_args = reqparse.RequestParser()
item_args.add_argument('item_name', type=str, required=True, help="Item name is required")
item_args.add_argument('sku', type=str)
item_args.add_argument('quantity', type=int, required=True, help="Item name is required")
item_args.add_argument('low_stock_threshold', type=int)
item_args.add_argument('category_id', type=int, required=True, help="Category ID is required")

class Items(Resource):
    def get(self, item_id=None):
        if item_id:
            item = Item.query.get_or_404(item_id)
            category = db.session.query(Item.category).filter_by(category_id=item.category_id).first()
            item.category_name = category[0] if category else "Unknown"
            return {col: getattr(item, col) for col in item.__table__.columns.keys()}
        items = Item.query.all()
        return [{col: getattr(i, col) for col in i.__table__.columns.keys()} for i in items]
    def post(self):
        args = item_args.parse_args()
        if args["item_name"].strip() == "":
            return {"message": "Item name cannot be empty"}, 400
        if args["quantity"] < 0:
            return {"message": "Quantity cannot be negative"}, 400
        if args["low_stock_threshold"] is not None and args["low_stock_threshold"] < 0:
            return {"message": "Low stock threshold cannot be negative"}, 400


        item = Item(**args)
        db.session.add(item)
        db.session.commit()
        return {"message": "Item created"},201
    
    def put(self,item_id):
        item = Item.query.get_or_404(item_id)
        args = item_args.parse_args()

        if "item_name" in args and args["item_name"] and args["item_name"].strip() == "":
            return {"message": "Item name cannot be empty"}, 400
        if "quantity" in args and args["quantity"] is not None and args["quantity"] < 0:
            return {"message": "Quantity cannot be negative"}, 400
        if "low_stock_threshold" in args and args["low_stock_threshold"] is not None and args["low_stock_threshold"] < 0:
            return {"message": "Low stock threshold cannot be negative"}, 400


        for key, value in args.items():
            setattr(item, key, value)
        db.session.commit()
        return {"message": "Item updated"}
    
    def delete(self, item_id):
        item = Item.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item deleted"}
    

lookup_args = reqparse.RequestParser()
lookup_args.add_argument('search', type=str, required=True, help="Search term is required")

class ItemLookup(Resource):
    def get(self):
        args = lookup_args.parse_args()
        search_term = args['search']
        items = Item.query.filter(
            (Item.item_name.ilike(f'%{search_term}%')) |
            (Item.category.ilike(f'%{search_term}%')) |
            (Item.sku.ilike(f'%{search_term}%'))
        ).all()
        return [{"item_id": item.item_id, "item_name": item.item_name,
        "category": item.category, "sku": item.sku, "quantity": item.quantity, "low_stock_threshold": item.low_stock_threshold, "category_id": item.category_id} for item in items], 200
