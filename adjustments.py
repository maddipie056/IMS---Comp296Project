from flask_restful import Resource, reqparse 
from models import Staff, StockAdjustment, Item
from app import db
from datetime import datetime
 

stock_adj_args = reqparse.RequestParser()
stock_adj_args.add_argument('item_id', type=int, required=True, help="Item ID is required")
stock_adj_args.add_argument('staff_id', type=int, required=True, help="Staff ID is required")
stock_adj_args.add_argument('change_amount', type=int, required=True, help="Change amount is required")
stock_adj_args.add_argument('action', type=str, required=True, help="Action must be 'increase' or 'decrease'")


class StockAdjustmentAPI(Resource):
    def get(self, adjustment_id=None):
        if adjustment_id:
            adj = StockAdjustment.query.get_or_404(adjustment_id)
            return {col: getattr(adj, col) for col in adj.__table__.columns.keys()}
        adjustments = StockAdjustmentAPI.query.all()
        return [{col: getattr(a, col) for col in a.__table__.columns.key()} for a in adjustments]
    def post(self):
        args = stock_adj_args.parse_args()
        item_id = args['item_id']
        staff_id = args['staff_id']
        amount = args['change_amount']
        action = args['action'].lower()

        if action not in ['increase', 'decrease']:
            return {"message": "Action must be 'increase' or 'decrease'"}, 400
        if amount <= 0:
            return {"message": "Amount must be greater than zero"}, 400
        
        item = Item.query.get(args['item_id'])
        if not item:
            return {"message": "Item not found"}, 404
        
        staff = Staff.query.get(args['staff_id'])
        if not staff:
            return {"message": "Staff not found"}, 404
        
        previous_quantity = item.quantity
        if action == 'increase':
            item.quantity += amount
        elif action == 'decrease':
            if item.quantity - amount < 0:
                return {"message": "Cannot reduce below zero"}, 400
            item.quantity -= amount

        adjustment = StockAdjustment(
            item_id=item_id,
            staff_id=staff_id,
            change_amount=amount if action == 'increase' else -amount,
            action=action,
            timestamp=datetime.utcnow()
        )
        db.session.add(adjustment)
        db.session.commit()

        return {"message": "Stock updated successfully", "item": {"id": item.id, "name": item.name, "quantity": item.quantity}, 
                "adjustment":{"id": adjustment.id, "action": adjustment.action, "amount": adjustment.change_amount, "previous_quantity": previous_quantity,
                              "new_quantity": item.quantity, "timestamp": adjustment.timestamp.isoformat()}}, 201

class StockAdjustmentListAPI(Resource):
    def get(self):
        adjustments = StockAdjustment.query.all()
        return [{col: getattr(a, col) for col in a.__table__.columns.keys()} for a in adjustments]
