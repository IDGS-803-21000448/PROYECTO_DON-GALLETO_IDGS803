from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import datetime

db= SQLAlchemy()


class Empleado(db.Model):
    __tablename__ = 'empleados'
    id=db.Column(db.Integer, primary_key = True)
    nombre= db.Column(db.String(50))
    email= db.Column(db.String(50))
    telefono= db.Column(db.String(10))
    direccion= db.Column(db.String(50))
    sueldo= db.Column(db.Float(50))
    create_date= db.Column(db.DateTime, default=datetime.datetime.now)


class Pedido(db.Model):
    __tablename__ = 'pedidos'
    id = db.Column(db.Integer, primary_key=True)
    cliente_nombre = db.Column(db.String(100))
    cliente_direccion = db.Column(db.String(100))
    cliente_telefono = db.Column(db.String(15))
    fecha_compra = db.Column(db.Date, default=datetime.datetime.now)
    total = db.Column(db.Float)
    confirmado = db.Column(db.Boolean, default=False)
    create_date = db.Column(db.DateTime, default=datetime.datetime.now)

class Pizza(db.Model):
    __tablename__ = 'pizzas'
    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedidos.id'))
    tamano_pizza = db.Column(db.String(20))
    ingredientes = db.Column(db.String(200))  # Podría ser una relación muchos a muchos si quieres mayor detalle
    numero_pizzas = db.Column(db.Integer)
    subtotal = db.Column(db.Float)
