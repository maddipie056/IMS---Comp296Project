from flask_restful import Resource, reqparse 
from models import StockAdjustment
from app import db
 

stock_adj_args = reqparse.RequestParser()
stock_adj_args.add_argument('item_id', type=int, required=True, help="Item ID is required")
stock_adj_args.add_argument('staff_id', type=int, required=True, help="Staff ID is required")
stock_adj_args.add_argument('change_amount', type=int, required=True, help="Change amount is required")

class StockAdjustment(Resource):
    def get(self, adjustment_id=None):
        if adjustment_id:
            adj = StockAdjustment.query.get_or_404(adjustment_id)
            return {col: getattr(adj, col) for col in adj.__table__.columns.keys()}
        adjustments = StockAdjustment.query.all()
        return [{col: getattr(a, col) for col in a.__table__columns.key()} for a in adjustments]
    def post(self):
        args = stock_adj_args.parse_args()
        adj = StockAdjustment(**args)
        db.session.add(adj)
        db.session.commit()
        return {"message": "Stock adjustment created"},201
    
    def put(self,adjustment_id):
        adj = StockAdjustment.query.get_or_404(adjustment_id)
        args = stock_adj_args.parse_args()
        for key, value in args.items():
            setattr(adj, key, value)
        db.session.commit()
        return {"message": "Stock adjustment updated"}
    
    def delete(self, adjustment_id):
        adj = StockAdjustment.query.get_or_404(adjustment_id)
        db.session.delete(adj)
        db.session.commit()
        return {"message": "Stock adjustment deleted"}
