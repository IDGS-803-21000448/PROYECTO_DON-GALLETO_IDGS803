from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import datetime
from flask_login import UserMixin

db = SQLAlchemy()

class Tipo_Materia(db.Model):
    __tablename__ = 'tipo_materia'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    tipo = db.Column(db.String(50))
    cantidad_disponible = db.Column(db.Float)
    estatus = db.Column(db.Integer, default=1)

class MateriaPrima(db.Model):
    __tablename__ = 'materias_primas'
    id = db.Column(db.Integer, primary_key=True)
    id_proveedor = db.Column(db.Integer, db.ForeignKey('proveedores.id'))
    id_tipo_materia = db.Column(db.Integer, db.ForeignKey('tipo_materia.id'))

    cantidad_disponible = db.Column(db.Float)
    cantidad_compra = db.Column(db.Float)
    tipo = db.Column(db.String(50))
    precio_compra = db.Column(db.Float)
    create_date = db.Column(db.Date, default=datetime.date.today())
    fecha_caducidad = db.Column(db.Date)
    lote = db.Column(db.String(50))

    estatus = db.Column(db.Integer, default=1)
    proveedor = db.relationship('Proveedor', backref=db.backref('MateriaPrima', lazy=True))
    tipo_materia = db.relationship('Tipo_Materia', backref=db.backref('MateriaPrima', lazy=True))


class Receta(db.Model):
    __tablename__ = 'recetas'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    descripcion = db.Column(db.Text)
    num_galletas = db.Column(db.Integer)
    imagen = db.Column(db.Text)
    create_date = db.Column(db.DateTime, default=datetime.datetime.now)
    estatus = db.Column(db.Integer, default=1)
    id_precio = db.Column(db.Integer, db.ForeignKey('costoGalletas.id'))
    Costo_Galleta = db.relationship('CostoGalleta', backref=db.backref('usos', lazy=True))


class RecetaDetalle(db.Model):
    __tablename__ = 'receta_detalle'
    id = db.Column(db.Integer, primary_key=True)
    receta_id = db.Column(db.Integer, db.ForeignKey('recetas.id'))
    tipo_materia_id = db.Column(db.Integer, db.ForeignKey('tipo_materia.id'))
    cantidad_necesaria = db.Column(db.Float)
    unidad_medida = db.Column(db.String(10))
    merma_porcentaje = db.Column(db.Float)
    receta = db.relationship('Receta', backref=db.backref('detalles', lazy=True))
    tipo_materia = db.relationship('Tipo_Materia', backref=db.backref('usos', lazy=True))

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
    galletas_disponibles = db.Column(db.Integer, default = 0)
    fecha_solicitud = db.Column(db.DateTime, default=datetime.datetime.now)
    fecha_producido = db.Column(db.DateTime, nullable=True)
    fecha_postergado = db.Column(db.DateTime, nullable=True)
    fecha_cancelado = db.Column(db.DateTime, nullable=True)
    lote = db.Column(db.String(50), nullable = True)
    empleadoSolicitante = db.Column(db.String(50), nullable = True)
    empleadoProduccion = db.Column(db.String(50), nullable = True)
    receta = db.relationship('Receta', backref=db.backref('produccion', lazy=True))
    
# class solicitudProduccion(db.Model):
#     __tablename__ = 'solicitudProduccion'
#     id = db.Column(db.Integer, primary_key=True)
#     fecha_solicitud = db.Column(db.DateTime, default=datetime.datetime.now, nullable=False)
#     receta_id = db.Column(db.Integer, db.ForeignKey('recetas.id'))
#     estatus = db.Column(db.String(50))


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
    produccion_id = db.Column(db.Integer, db.ForeignKey('produccion.id'))
    cantidad = db.Column(db.Float)
    descripcion = db.Column(db.String(200), nullable=True)
    fecha = db.Column(db.DateTime, default=datetime.datetime.now)
    tipo = db.Column(db.String(50))
    estatus = db.Column(db.Integer, default=1)
    produccion = db.relationship('Produccion', backref=db.backref('mermas', lazy=True))
    

#-------PROVEEDORES--------
class Proveedor(db.Model):
    __tablename__ = 'proveedores'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    direccion = db.Column(db.String(255))
    telefono = db.Column(db.String(15))
    nombre_vendedor = db.Column(db.String(100))
    estatus = db.Column(db.Integer, default=1)
    
#-------VENTAS-------
class Turnos(db.Model):
    __tablename__ = 'turnos'
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, default=datetime.datetime.now)
    estatus = db.Column(db.String(100), default='En turno') # En turno, completado
    fondo_caja = db.Column(db.Float, nullable=False)
    venta_total = db.Column(db.Float, nullable=False, default=0)
    salidas_totales = db.Column(db.Float, nullable=False, default=0)
    total_final = db.Column(db.Float, nullable=False, default=0)
    id_usuario = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)    

class Salidas(db.Model):
    __tablename__ = 'salidas'
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, default=datetime.datetime.now)
    cantidad = db.Column(db.Float, nullable=False)
    justificacion = db.Column(db.Text, nullable=False)
    id_turno = db.Column(db.Integer, db.ForeignKey('turnos.id'), nullable=False)

class Venta(db.Model):
    __tablename__ = 'venta'
    id = db.Column(db.Integer, primary_key=True)
    folio = db.Column(db.String(8))
    nombre_cliente = db.Column(db.String(50))
    fecha = db.Column(db.DateTime, default=datetime.datetime.now)
    total = db.Column(db.Float)
    id_turno = db.Column(db.Integer, db.ForeignKey('turnos.id'), nullable=False)

class DetalleVenta(db.Model):
    __tablename__ = 'detalle_venta'
    id = db.Column(db.Integer, primary_key=True)
    sabor = db.Column(db.String(255), nullable=False)
    tipo_venta = db.Column(db.String(50), nullable=False)
    precio_unitario = db.Column(db.Float, nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    cantidad_galletas = db.Column(db.Integer, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)
    venta_id = db.Column(db.Integer, db.ForeignKey('venta.id'), nullable=False)
    receta_id = db.Column(db.Integer, db.ForeignKey('recetas.id'))

class CostoGalleta(db.Model):
    __tablename__ = 'costoGalletas'
    id = db.Column(db.Integer, primary_key=True)
    precio = db.Column(db.Float)
    galletas_disponibles = db.Column(db.Integer)
    mano_obra = db.Column(db.Float)
    fecha_utlima_actualizacion = db.Column(db.DateTime, default=datetime.datetime.now)

# -------LOGS-------
class LogLogin(db.Model):
    __tablename__ = 'log_login'
    id = db.Column(db.Integer, primary_key=True)
    log = db.Column(db.Text, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.datetime.now, nullable=False)
    ip = db.Column(db.String(15), nullable=False)
    direccion = db.Column(db.String(255), nullable=False)
    estatus = db.Column(db.String(50), nullable=False) # correcto, incorrecto
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
