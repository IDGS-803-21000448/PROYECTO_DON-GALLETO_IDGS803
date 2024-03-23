from flask import Blueprint


galletas = Blueprint('galletas', __name__, template_folder="../templates")
from . import routes