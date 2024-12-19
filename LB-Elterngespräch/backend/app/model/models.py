# coding: utf-8
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from model.ACCESS import ACCESS


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

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    access = db.Column(db.SmallInteger, nullable=False, default=0)

    def is_admin(self):
        return self.access == ACCESS['admin']
    
    def is_teacher(self):
        return self.access == ACCESS['lehrer']

    def is_guest(self):
        return self.access == ACCESS['guest']

    def allowed(self, access_level):
        return self.access >= access_level
    

class ElterngespraechTermine(db.Model):
    __tablename__ = 'elterngespraech_termine'
    termin_id = db.Column(db.Integer, primary_key=True)
    lehrer_id = db.Column(db.Integer, nullable=False)
    schueler_name = db.Column(db.String(30), nullable=False)
    datum = db.Column(db.Date, nullable=False)
    uhrzeit = db.Column(db.Time, nullable=False)
    dauer_minuten = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    raum = db.Column(db.String(20), nullable=False)
    notizen = db.Column(db.Text, nullable=False)
