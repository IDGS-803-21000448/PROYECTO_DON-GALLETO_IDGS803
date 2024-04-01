from flask import render_template
from . import dashboard
from flask_login import login_required, current_user
from controllers.controller_login import requiere_token
from models import LogLogin

@dashboard.route("/dashboard", methods=["GET"])
@login_required
@requiere_token
def dashboard():
    # obtener logs de inicio de sesión correctos del usuario
    logs = LogLogin.query.filter_by(id_user=current_user.id, estatus='correcto').order_by(LogLogin.id.desc()).limit(2).all()

    # obtener el segundo ultimo log de inicio de sesion correcto del usuario
    if len(logs) > 1:
        # regresar lastSession en formato dd/mm/yyyy hh:mm:ss
        lastSession = logs[1].fecha.strftime("%d/%m/%Y %H:%M:%S")
    else:
        lastSession = None

    return render_template("moduloDashboard/dashboard.html", lastSession=lastSession)