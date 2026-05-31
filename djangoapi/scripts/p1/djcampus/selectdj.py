# scripts/p1/djcampus/selectdj.py
# Consultas con Django ORM para puntos, lineas y poligonos.
# Se ejecuta con: python manage.py runscript scripts.p1.djcampus.selectdj --script-args poligonos 1

from django.forms.models import model_to_dict
from campus.models import Punto, Linea, Poligono


def object_to_dict(obj):
    d = model_to_dict(obj)
    d["geom"] = obj.geom.wkt
    return d


def select_data(model, id_value):
    # id_value = 0 devuelve todos los registros.
    # id_value > 0 devuelve solo el registro con ese id.
    if id_value == 0:
        lista = list(model.objects.filter(id__gt=0).order_by("id"))
    else:
        lista = list(model.objects.filter(id=id_value))

    if len(lista) == 0:
        return {"ok": False, "message": "No se encontraron registros", "data": []}

    data = [object_to_dict(obj) for obj in lista]
    return {"ok": True, "message": "Datos recuperados", "data": data}


def run(*args):
    if len(args) < 1:
        print("Uso: --script-args puntos|lineas|poligonos [id]")
        return

    tabla = args[0].lower()
    id_buscado = int(args[1]) if len(args) > 1 else 0

    tablas = {
        "puntos": Punto,
        "lineas": Linea,
        "poligonos": Poligono,
    }

    if tabla in tablas:
        print(select_data(tablas[tabla], id_buscado))
    else:
        print("Tabla no valida")

# python manage.py runscript scripts.p1.djcampus.selectdj --script-args poligonos 1
