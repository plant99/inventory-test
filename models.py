from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()



class Product(db.Model):

    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # for simplicity, I've considered only one row for Product table
    name = db.Column(db.String(255), unique=True)

    def __init__(self, name):
        """
        name: name of the product
        """
        self.name = name

    def __repr__(self):
        return('<Product name {}>'.format(self.name))

class Location(db.Model):

    __tablename__ = "locations"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # for simplicity, I've considered only one row for Location table
    name = db.Column(db.String(255), unique=True)

    def __init__(self, name):
        """
        name: name of the product
        """
        self.name = name

    def __repr__(self):
        return('<Location name {}>'.format(self.name))



class ProductMovement(db.Model):

    __tablename__ = 'product_movements'
    movement_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    qty = db.Column(db.Integer)
    from_location = db.Column(db.Integer, db.ForeignKey('locations.id', ondelete="cascade"), nullable=True)
    to_location = db.Column(db.Integer, db.ForeignKey('locations.id', ondelete="cascade"), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, product_id, from_location, to_location, qty=0):
        """
        product_id: product id
        qty: quantity of product
        from_location: from location id
        to_location: to location id
        timestamp: last updated timestamp
        """
        self.product_id = product_id
        self.qty = qty
        self.from_location = from_location
        self.to_location = to_location

    def __repr__(self):
        return('<ProductMovement id {self.movement_id}')
