from flask import Blueprint


solicitud_produccion = Blueprint('solicitudProduccion', __name__, template_folder="../templates")
from . import routes