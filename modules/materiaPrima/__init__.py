from flask import Blueprint


materia_prima = Blueprint('materiaPrima', __name__, template_folder="../templates")
from . import routes