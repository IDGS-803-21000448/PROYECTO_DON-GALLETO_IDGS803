import json

from flask import render_template

from controllers import controller_mermas
from . import mermas

@mermas.route('/moduloMermas')
def crud_mermas():
    return render_template('moduloMermas/crudMermas.html')

@mermas.route("/pruebaCaducidades", methods=["GET"])
def pruebaCaducidades():
    resultado = controller_mermas.verificarCaducidades()
    return json.dumps(resultado)