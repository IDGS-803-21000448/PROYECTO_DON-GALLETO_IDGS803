from flask import Blueprint


stock = Blueprint('stock', __name__, template_folder="../templates")
from . import routes