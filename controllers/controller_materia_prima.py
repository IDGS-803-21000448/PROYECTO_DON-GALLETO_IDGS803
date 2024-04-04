
from sqlalchemy import not_
import models
from models import *
from datetime import date
from controllers.controller_alertas import insertarAlertas

def actualizar_cantidades_tipo():

    materiasPrimas = MateriaPrima.query.filter(models.MateriaPrima.estatus != 0).all()
    tipos_materias = Tipo_Materia.query.filter_by(estatus = 1).all()
    try:

        for tipo in tipos_materias:
            suma = 0
            for materia in materiasPrimas:
               if materia.id_tipo_materia == tipo.id:
                   if materia.tipo == tipo.tipo:
                     suma += materia.cantidad_disponible
                   else:
                       suma += convertirCantidades(tipo.tipo, materia.tipo, materia.cantidad_disponible)
            tipo.cantidad_disponible= suma
            db.session.commit()
    except Exception as e:
        print("Error al verificar las caducidades: ", e)



def convertirCantidades(tipo1, tipo2, cantidad):
    if (tipo1 == "g" or tipo1 == "ml") and (tipo2 == "kg" or tipo2 == "l"):
        cantidad = cantidad * 1000
    elif (tipo1 == "kg" or tipo1 == "l") and (tipo2 == "g" or tipo2 == "ml"):
        cantidad = cantidad / 1000

    return cantidad



