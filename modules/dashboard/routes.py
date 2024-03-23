from flask import render_template
from . import dashboard

@dashboard.route("/dashboard", methods=["GET"])
def dashboard():
    return render_template("moduloDashboard/dashboard.html")