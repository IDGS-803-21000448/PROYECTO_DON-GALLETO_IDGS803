from flask import Blueprint


alertas = Blueprint('alertas', __name__, template_folder="../templates")
from . import routes