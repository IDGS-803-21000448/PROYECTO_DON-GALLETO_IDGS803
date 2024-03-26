from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import datetime
from flask_login import UserMixin

db = SQLAlchemy()

class MateriaPrima(db.Model):
    __tablename__ = 'materias_primas'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    fecha_caducidad = db.Column(db.Date)
    cantidad_disponible = db.Column(db.Float)
    tipo = db.Column(db.String(50))
    create_date = db.Column(db.DateTime, default=datetime.datetime.now)
    estatus = db.Column(db.Integer, default=1)


class Receta(db.Model):
    __tablename__ = 'recetas'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    descripcion = db.Column(db.Text)
    num_galletas = db.Column(db.Integer)
    imagen = db.Column(db.Text)
    create_date = db.Column(db.DateTime, default=datetime.datetime.now)
    estatus = db.Column(db.Integer, default=1)

class RecetaDetalle(db.Model):
    __tablename__ = 'receta_detalle'
    id = db.Column(db.Integer, primary_key=True)
    receta_id = db.Column(db.Integer, db.ForeignKey('recetas.id'))
    materia_prima_id = db.Column(db.Integer, db.ForeignKey('materias_primas.id'))
    cantidad_necesaria = db.Column(db.Float)
    unidad_medida = db.Column(db.String(10))
    merma_porcentaje = db.Column(db.Float)
    receta = db.relationship('Receta', backref=db.backref('detalles', lazy=True))
    materia_prima = db.relationship('MateriaPrima', backref=db.backref('usos', lazy=True))

class MermaMateriaPrima(db.Model):
    __tablename__ = 'mermaMateriaPrima'
    id = db.Column(db.Integer, primary_key=True)
    materia_prima_id = db.Column(db.Integer, db.ForeignKey('materias_primas.id'))
    cantidad = db.Column(db.Float)
    descripcion = db.Column(db.String(200), nullable=True)
    tipo = db.Column(db.String(50))
    fecha = db.Column(db.DateTime, default=datetime.datetime.now)
    estatus = db.Column(db.Integer, default=1)
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


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    puesto = db.Column(db.String(80), nullable=False)
    rol = db.Column(db.String(80), nullable=False)
    estatus = db.Column(db.String(80), nullable=False)
    usuario = db.Column(db.String(80), nullable=False)
    contrasena = db.Column(db.String(80), nullable=False)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        # Aquí puedes agregar lógica para deshabilitar usuarios si es necesario
        if self.estatus == "Activo":
            return True
        else:
            return False

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        # Flask-Login espera que el identificador sea una cadena, por eso la conversión
        return str(self.id)

class Alerta(db.Model):
    __tablename__ = 'alertas'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    descripcion = db.Column(db.String(200))
    fechaAlerta = db.Column(db.DateTime, default=datetime.datetime.now)
    estatus = db.Column(db.Integer, default=1)


class MemraGalleta(db.Model):
    __tablename__ = 'mermaGalletas'
    id = db.Column(db.Integer, primary_key=True)
    receta_id = db.Column(db.Integer, db.ForeignKey('recetas.id'))
    cantidad = db.Column(db.Float)
    descripcion = db.Column(db.String(200), nullable=True)
    fecha = db.Column(db.DateTime, default=datetime.datetime.now)
    tipo = db.Column(db.String(50))
    estatus = db.Column(db.Integer, default=1)
    materia_prima = db.relationship('Receta', backref=db.backref('mermas', lazy=True))
    

#-------PROVEEDORES--------
class Proveedor(db.Model):
    __tablename__ = 'proveedores'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    direccion = db.Column(db.String(255))
    telefono = db.Column(db.String(15))
    nombre_vendedor = db.Column(db.String(100))
    estatus = db.Column(db.Integer, default=1)
    