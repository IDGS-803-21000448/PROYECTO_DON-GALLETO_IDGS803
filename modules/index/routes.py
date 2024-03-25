from flask import render_template

from controllers import controller_mermas
from . import index

@index.route('/index', methods=["GET"])
def index():
    controller_mermas.verificarCaducidades()
    return render_template("index.html")