from flask import Blueprint


inventarios = Blueprint('inventarios', __name__, template_folder="../templates")
from . import routes