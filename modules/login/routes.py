from flask import render_template
from . import login

@login.route("/login", methods=["GET"])
def login():
    return render_template("moduloLogin/login.html")