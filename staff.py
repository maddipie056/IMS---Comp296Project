from flask_restful import Resource, reqparse
from apps.models import Staff
from apps import db


staff_args = reqparse.RequestParser()
staff_args.add_argument('username', type=str, required=True, help="Username cannot be blank")
staff_args.add_argument('password_hash', type=str, required=True, help="Password is required")
staff_args.add_argument('role', type=str, required=True, help="Role is required")

class Staff(Resource):
    def get(self, staff_id=None):
        if staff_id:
            staff = Staff.query.get_or_404(staff_id)
            return {col: getattr(staff, col) for col in staff.__table__.columns.keys()}
        staff_list = Staff.query.all()
        return [{col: getattr(s, col) for col in s.__table__columns.key()} for s in staff_list]
    def post(self):
        args = staff_args.parse_args()
        staff = Staff(**args)
        db.session.add(staff)
        db.session.commit()
        return {"message": "Staff created"},201
    
    def put(self,staff_id):
        staff = Staff.query.get_or_404(staff_id)
        args = staff_args.parse_args()
        for key, value in args.items():
            setattr(staff, key, value)
        db.session.commit()
        return {"message": "Staff updated"}
    
    def delete(self, staff_id):
        staff = Staff.query.get_or_404(staff_id)
        db.session.delete(staff)
        db.session.commit()
        return {"message": "Staff deleted"}
