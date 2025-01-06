# backend/app/model/models.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class Productline(db.Model):
    __tablename__ = 'productlines'

    productLine = db.Column(db.String(50), primary_key=True)
    textDescription = db.Column(db.String(4000))
    htmlDescription = db.Column(db.String)
    #image = db.Column(db.MEDIUMBLOB)


class Product(db.Model):
    __tablename__ = 'products'

    productCode = db.Column(db.String(15), primary_key=True)
    productName = db.Column(db.String(70), nullable=False)
    productLine = db.Column(db.ForeignKey('productlines.productLine'), nullable=False, index=True)
    productScale = db.Column(db.String(10), nullable=False)
    productVendor = db.Column(db.String(50), nullable=False)
    productDescription = db.Column(db.Text, nullable=False)
    quantityInStock = db.Column(db.SmallInteger, nullable=False)
    buyPrice = db.Column(db.Numeric(10, 2), nullable=False)
    MSRP = db.Column(db.Numeric(10, 2), nullable=False)

    productline = db.relationship('Productline', primaryjoin='Product.productLine == Productline.productLine', backref='products')

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False, default="parent")  # parent, teacher, admin
    teacher_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  # Stammlehrer für Eltern

    # Relation für Lehrer
    teacher = db.relationship("User", remote_side=[id], backref="students")

class Termin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  # Parent claiming the Termin

    teacher = db.relationship("User", foreign_keys=[teacher_id], backref="termine")
    parent = db.relationship("User", foreign_keys=[parent_id])  # Relation to Parent User

