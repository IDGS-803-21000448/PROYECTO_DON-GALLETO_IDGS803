from flask import render_template
from . import index

@index.route('/index', methods=["GET"])
def index():
    return render_template("index.html")