from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import datetime

db = SQLAlchemy()

class MateriaPrima(db.Model):
    __tablename__ = 'materias_primas'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    fecha_caducidad = db.Column(db.Date)
    cantidad_disponible = db.Column(db.Float)
    create_date = db.Column(db.DateTime, default=datetime.datetime.now)

class Receta(db.Model):
    __tablename__ = 'recetas'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    descripcion = db.Column(db.Text)
    num_galletas = db.Column(db.Integer)
    create_date = db.Column(db.DateTime, default=datetime.datetime.now)

class RecetaDetalle(db.Model):
    __tablename__ = 'receta_detalle'
    id = db.Column(db.Integer, primary_key=True)
    receta_id = db.Column(db.Integer, db.ForeignKey('recetas.id'))
    materia_prima_id = db.Column(db.Integer, db.ForeignKey('materias_primas.id'))
    cantidad_necesaria = db.Column(db.Float)
    merma_porcentaje = db.Column(db.Float)
    
    receta = db.relationship('Receta', backref=db.backref('detalles', lazy=True))
    materia_prima = db.relationship('MateriaPrima', backref=db.backref('usos', lazy=True))

class Merma(db.Model):
    __tablename__ = 'mermas'
    id = db.Column(db.Integer, primary_key=True)
    materia_prima_id = db.Column(db.Integer, db.ForeignKey('materias_primas.id'))
    tipo = db.Column(db.String(50))
    cantidad = db.Column(db.Float)
    descripcion = db.Column(db.String(200), nullable=True)
    fecha = db.Column(db.DateTime, default=datetime.datetime.now)

    materia_prima = db.relationship('MateriaPrima', backref=db.backref('mermas', lazy=True))

class Produccion(db.Model):
    __tablename__ = 'produccion'
    id = db.Column(db.Integer, primary_key=True)
    receta_id = db.Column(db.Integer, db.ForeignKey('recetas.id'))
    estatus = db.Column(db.String(50)) # 4 Estatus solicitud, produccion, producido, postergado
    cantidad = db.Column(db.Integer)
    fecha_solicitud = db.Column(db.DateTime, default=datetime.datetime.now)
    fecha_producido = db.Column(db.DateTime, nullable=True)
    fecha_postergado = db.Column(db.DateTime, nullable=True)
