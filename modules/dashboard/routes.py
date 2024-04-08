from flask import render_template, session
from sqlalchemy import func

from . import dashboard
from flask_login import login_required, current_user
from controllers.controller_login import requiere_token
from models import LogLogin, Alerta, CostoGalleta, Receta, RecetaDetalle, MateriaPrima, MemraGalleta, db, Produccion


@dashboard.route("/dashboard", methods=["GET"])
@login_required
@requiere_token
def dashboard():
    # obtener logs de inicio de sesión correctos del usuario
    logs = LogLogin.query.filter_by(id_user=current_user.id, estatus='correcto').order_by(LogLogin.id.desc()).limit(2).all()
    mermas_mayor = obtenerMayorMerma()
    merma_porcentaje = obtenerMermaPorcentaje()
    costos_galletas = obtenerCostos()

    # obtener el segundo ultimo log de inicio de sesion correcto del usuario
    if len(logs) > 1:
        # regresar lastSession en formato dd/mm/yyyy hh:mm:ss
        lastSession = logs[1].fecha.strftime("%d/%m/%Y %H:%M:%S")
    else:
        lastSession = None
    alertas = Alerta.query.filter_by(estatus = 0).all()
    session['countAlertas'] = len(alertas)
    return render_template("moduloDashboard/dashboard.html", lastSession=lastSession, costos_galletas=costos_galletas, merma_mayor=mermas_mayor, merma_porcentaje = merma_porcentaje)



def obtenerMayorMerma():
    result = db.session.query(
        Receta.nombre,
        func.sum(MemraGalleta.cantidad).label('total_merma')
    ).join(
        Produccion, MemraGalleta.produccion_id == Produccion.id
    ).join(
        Receta, Produccion.receta_id == Receta.id
    ).group_by(
        Receta.nombre
    ).order_by(
        func.sum(MemraGalleta.cantidad).desc()
    ).all()
    resultados_serializables = []
    for nombre, total_merma in result:

        resultados_serializables.append((nombre, total_merma))

    return resultados_serializables


def obtenerMermaPorcentaje():
    cantidad_producciones_subq = db.session.query(
        Receta.id.label('id_receta'),
        func.count('*').label('cantidad_producciones')
    ).join(
        Produccion, Produccion.receta_id == Receta.id
    ).group_by(
        Receta.id
    ).subquery()

    result = db.session.query(
        Receta.nombre,
        (func.sum(MemraGalleta.cantidad) * 100) / (
                    func.max(cantidad_producciones_subq.c.cantidad_producciones) * func.max(
                Receta.num_galletas)).label('porcentaje_merma')
    ).join(
        Produccion, MemraGalleta.produccion_id == Produccion.id
    ).join(
        Receta, Produccion.receta_id == Receta.id
    ).join(
        cantidad_producciones_subq, Receta.id == cantidad_producciones_subq.c.id_receta
    ).group_by(
        Receta.nombre
    ).all()

    resultados_serializables = []
    for nombre, total_merma in result:
        resultados_serializables.append((nombre, total_merma))

    return resultados_serializables

def obtenerCostos():
    # Lista para almacenar los costos de recetas
    costos_recetas = []

    # Obtenemos todas las recetas con estatus 1
    recetas = Receta.query.filter_by(estatus=1).all()

    # Vamos a recorrer todas las recetas
    for receta in recetas:
        # Obtener los detalles de la receta
        detalles_receta = RecetaDetalle.query.filter_by(receta_id=receta.id).all()
        # Obtener los IDs de los ingredientes de la receta seleccionada
        ids_ingredientes = [detalle.tipo_materia_id for detalle in detalles_receta]
        # Obtener los costos de la receta y sus detalles
        costos = CostoGalleta.query.filter_by(id=receta.id).first()
        factor_ajuste_mano_obra = 0.5  # Factor de ajuste para la mano de obra

        # Inicializar variables
        suma_costos = 0
        cantidad_materias = 0
        costo_mano_obra = 0

        # Realizar la consulta de Materias Prima para cada ID de ingrediente
        for id_ingrediente in ids_ingredientes:
            # Obtener las materias primas que corresponden al ID de ingrediente
            materias = MateriaPrima.query.filter_by(id_tipo_materia=id_ingrediente, estatus=1).all()

            # Si las materias primas existen
            if materias:
                # Obtener el total de precio de la materia
                total_precio_materia = sum(m.precio_compra for m in materias)
                # Obtener el total de cantidades de la materia
                cantidad_materias += len(materias)

                # Puede haber varias compras de la misma materia
                for materia in materias:
                    # Obtenemos el detalle de receta de la receta que estamos iterando
                    detalles_receta = RecetaDetalle.query.filter_by(receta_id=receta.id, tipo_materia_id=id_ingrediente).first()
                    cantidad_materia = convertirCantidades(materia.tipo, detalles_receta.unidad_medida, detalles_receta.cantidad_necesaria)

                    # Calcular el precio por kilogramo/litro
                    precio_por_kg = total_precio_materia / cantidad_materia

                    # Aplicar el factor de ajuste a la mano de obra
                    if costos.mano_obra is None:
                        # Manejar el caso en que el valor de mano_obra sea None, por default será 100
                        mano_obra = costos.mano_obra = 100
                    else:
                        mano_obra = costos.mano_obra

                    # asignamos el factor de ajuste de la mano de obra
                    costo_mano_obra = mano_obra * factor_ajuste_mano_obra

                    # Calcular el costo de los ingredientes
                    costo_ingredientes = ((cantidad_materia * precio_por_kg) + costo_mano_obra) / materia.cantidad_compra

                    # Agregar el costo de la materia a la suma de costos
                    suma_costos += costo_ingredientes

        # Calcular el costo promedio de la receta
        costo_receta = round(suma_costos / cantidad_materias, 2)
        # Guardar el costo de la receta junto con su nombre en la lista
        costos_recetas.append((receta.nombre, costo_receta))

    return costos_recetas

def convertirCantidades(tipo1, tipo2, cantidad):
    if (tipo1 == "g" or tipo1 == "ml") and (tipo2 == "kg" or tipo2 == "l"):
        cantidad = cantidad * 1000
    elif (tipo1 == "kg" or tipo1 == "l") and (tipo2 == "g" or tipo2 == "ml"):
        cantidad = cantidad / 1000
    elif(tipo1 == "pz") and (tipo2 == "kg" or tipo2 == "l"):
        cantidad = cantidad / 1000
        cantidad = cantidad / 50
    elif(tipo1 == "pz") and (tipo2 == "g" or tipo2 == "ml"):
        cantidad = cantidad / 50
    elif(tipo1 == "g" or tipo1 == "ml") and (tipo2 == "pz"):
        cantidad = cantidad * 50
    elif(tipo1 == "kg" or tipo1 == "l") and (tipo2 == "pz"):
        cantidad = cantidad * 0.050
    return cantidad