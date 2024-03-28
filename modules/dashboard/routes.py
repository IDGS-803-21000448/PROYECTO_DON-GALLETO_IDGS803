from flask import render_template
from . import dashboard
from flask_login import login_required
from controllers.controller_login import requiere_token

@dashboard.route("/dashboard", methods=["GET"])
@login_required
@requiere_token
def dashboard():
    return render_template("moduloDashboard/dashboard.html")