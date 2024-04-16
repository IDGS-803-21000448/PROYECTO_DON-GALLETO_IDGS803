from datetime import date

import models
from models import db

def insertarAlertas(nombre, descripcion, merma = False):
    nuevaAlerta = models.Alerta(
            nombre = f"{nombre}",
            descripcion = f"{descripcion} ",
            estatus = 0
    )
    if merma:
        alerta_existente = models.Alerta.query.filter_by(descripcion=descripcion).first()
        if not alerta_existente:
            nuevaAlerta = models.Alerta(
                nombre=nombre,
                descripcion=descripcion,
                estatus=0
            )
            db.session.add(nuevaAlerta)
    else:
        db.session.add(nuevaAlerta)
    db.session.commit()


def verificarCantidades():
    materiasPrimas = models.Tipo_Materia.query.filter_by(estatus = 1).all()  #Obtiene La materia prima que no esta en merma Aún
    fecha_actual = date.today() # Fecha De Hoy
    try:
        for materiaPrima in materiasPrimas:

            if (materiaPrima.tipo == 'kg' or materiaPrima.tipo == 'l') and materiaPrima.cantidad_disponible < 10:

                insertarAlertas("Alerta por Cantidad", f"Se esta a punto de terminar la materia prima de: "
                                                       f"{materiaPrima.nombre} solo hay {materiaPrima.cantidad_disponible}{materiaPrima.tipo}"
                                                       f" a dia de {fecha_actual}", True)

            elif (materiaPrima.tipo == 'g' or materiaPrima.tipo == 'ml') and materiaPrima.cantidad_disponible < 10000:
                insertarAlertas("Alerta por Cantidad", f"Se esta a punto de terminar la materia prima de: "
                                                       f"{materiaPrima.nombre} solo hay {materiaPrima.cantidad_disponible}{materiaPrima.tipo}"
                                                       f" a dia de {fecha_actual}", True)

    except Exception as e:
        print("Error al verificar las caducidades: ", e)



def verificarCantidadesGalletas():
    recetas = models.Receta.query.filter_by(estatus = 1).all()
    fecha_actual = date.today() # Fecha De Hoy
    try:
        for receta in recetas:

            if receta.Costo_Galleta.galletas_disponibles < receta.num_galletas:

                insertarAlertas("Alerta por Cantidad", f"Se esta a punto de terminar la galleta de "
                                                       f"{receta.nombre} solo hay {receta.Costo_Galleta.galletas_disponibles } galletas"
                                                       f" a dia de {fecha_actual}", True)

    except Exception as e:
        print("Error al verificar las caducidades: ", e)