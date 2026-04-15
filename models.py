from apps import db

class Item(db.Model):
    __table__ = db.Model.metadata.tables['items']

class Staff(db.Model):
    __table__ = db.Model.metadata.tables['staff']

class StockAdjustment(db.Model):
    __table__ = db.Model.metadata.tables['stock_adjustments']

class Category(db.Model):
    __table__ = db.Model.metadata.tables['categories']
