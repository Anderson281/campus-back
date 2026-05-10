# scripts/p1/djcampus/deletedj.py
# Eliminaciones con Django ORM.
# Se ejecuta con: python manage.py runscript scripts.p1.djcampus.deletedj --script-args puntos 1

from campus.models import Punto, Linea, Poligono


def delete_data(model, id_value):
    qs = model.objects.filter(id=id_value)
    lista = list(qs)

    if len(lista) < 1:
        return {"ok": False, "message": f"No se encontro el registro con ID {id_value}", "data": []}

    obj = lista[0]
    obj.delete()
    return {"ok": True, "message": "Registro eliminado con exito", "data": [{"id": id_value}]}


def run(*args):
    if len(args) < 1:
        print("Uso: --script-args puntos|lineas|poligonos [id]")
        return

    tabla = args[0].lower()
    id_a_borrar = int(args[1]) if len(args) > 1 else 1

    tablas = {
        "puntos": Punto,
        "lineas": Linea,
        "poligonos": Poligono,
    }

    if tabla in tablas:
        print(delete_data(tablas[tabla], id_a_borrar))
    else:
        print("Tabla no valida")
