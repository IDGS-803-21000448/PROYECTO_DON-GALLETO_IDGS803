from flask import render_template
from . import dashboard
from flask_login import login_required

@dashboard.route("/dashboard", methods=["GET"])
@login_required
def dashboard():
    return render_template("moduloDashboard/dashboard.html")