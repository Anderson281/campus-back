# scripts/p1/djcampus/updatedj.py
# Actualizaciones con Django ORM + validaciones espaciales en PostGIS.
# Se ejecuta con: python manage.py runscript scripts.p1.djcampus.updatedj --script-args poligonos 1

from django.contrib.gis.geos import GEOSGeometry
from django.forms.models import model_to_dict
from django.db import connection
from campus.models import Punto, Linea, Poligono
from scripts.p1.myLib.p1Settings import EPSG_CODE, SNAP_DISTANCE


def parse_bool(value):
    if isinstance(value, bool):
        return value
    return str(value).lower() in ["true", "1", "si", "sí", "yes"]


def snap_geom(geom_wkt):
    cur = connection.cursor()
    cur.execute(
        """
        SELECT ST_AsText(
            ST_SnapToGrid(ST_GeomFromText(%s, %s), %s)
        )
        """,
        [geom_wkt, EPSG_CODE, SNAP_DISTANCE],
    )
    snapped_wkt = cur.fetchone()[0]
    return GEOSGeometry(snapped_wkt, srid=EPSG_CODE)


def model_to_dict_with_geom(obj):
    d = model_to_dict(obj)
    d["geom"] = obj.geom.wkt
    return d


def update_punto(d):
    try:
        g = snap_geom(d["geom"])
        if not g.valid:
            return {"ok": False, "message": "Geometria de punto invalida", "data": []}

        cur = connection.cursor()
        cur.execute(
            """
            SELECT id
            FROM campus_poligonos
            WHERE ST_Within(
                ST_SnapToGrid(ST_GeomFromText(%s, %s), %s),
                geom
            )
            LIMIT 1
            """,
            [d["geom"], EPSG_CODE, SNAP_DISTANCE],
        )
        if len(cur.fetchall()) == 0:
            return {"ok": False, "message": "El punto debe estar dentro de un poligono", "data": []}

        qs = Punto.objects.filter(id=d["id"])
        if not qs.exists():
            return {"ok": False, "message": "No existe el punto", "data": []}

        obj = qs[0]
        obj.tipo = d["tipo"]
        obj.estado = d["estado"]
        obj.material = d.get("material")
        obj.codigo_inventario = d["codigo_inventario"]
        obj.observacion = d.get("observacion")
        obj.geom = g
        obj.save()
        return {"ok": True, "message": "Punto actualizado", "data": [model_to_dict_with_geom(obj)]}
    except Exception as e:
        return {"ok": False, "message": str(e), "data": []}


def update_linea(d):
    try:
        g = snap_geom(d["geom"])
        if not g.valid:
            return {"ok": False, "message": "Geometria de linea invalida", "data": []}

        cur = connection.cursor()
        cur.execute(
            """
            SELECT id
            FROM campus_lineas
            WHERE ST_Relate(
                geom,
                ST_SnapToGrid(ST_GeomFromText(%s, %s), %s),
                'T********'
            )
            AND id != %s
            """,
            [d["geom"], EPSG_CODE, SNAP_DISTANCE, d["id"]],
        )
        rows = cur.fetchall()
        if len(rows) > 0:
            return {"ok": False, "message": "La linea se interseca con otra linea", "data": rows}

        qs = Linea.objects.filter(id=d["id"])
        if not qs.exists():
            return {"ok": False, "message": "No existe la linea", "data": []}

        obj = qs[0]
        obj.tipo_via = d["tipo_via"]
        obj.pavimento = d.get("pavimento")
        obj.accesible = parse_bool(d.get("accesible", True))
        obj.codigo_tramo = d["codigo_tramo"]
        obj.observacion = d.get("observacion")
        obj.geom = g
        obj.save()
        return {"ok": True, "message": "Linea actualizada", "data": [model_to_dict_with_geom(obj)]}
    except Exception as e:
        return {"ok": False, "message": str(e), "data": []}


def update_poligono(d):
    try:
        g = snap_geom(d["geom"])
        if not g.valid:
            return {"ok": False, "message": "Geometria de poligono invalida", "data": []}

        cur = connection.cursor()
        cur.execute(
            """
            SELECT id
            FROM campus_poligonos
            WHERE ST_Relate(
                geom,
                ST_SnapToGrid(ST_GeomFromText(%s, %s), %s),
                'T********'
            )
            AND id != %s
            """,
            [d["geom"], EPSG_CODE, SNAP_DISTANCE, d["id"]],
        )
        rows = cur.fetchall()
        if len(rows) > 0:
            return {"ok": False, "message": "El poligono se interseca con otro poligono", "data": rows}

        qs = Poligono.objects.filter(id=d["id"])
        if not qs.exists():
            return {"ok": False, "message": "No existe el poligono", "data": []}

        obj = qs[0]
        obj.nombre = d["nombre"]
        obj.uso_principal = d.get("uso_principal")
        obj.pisos = int(d["pisos"]) if d.get("pisos") not in [None, ""] else None
        obj.estado = d.get("estado")
        obj.observacion = d.get("observacion")
        obj.geom = g
        obj.save()
        return {"ok": True, "message": "Poligono actualizado", "data": [model_to_dict_with_geom(obj)]}
    except Exception as e:
        return {"ok": False, "message": str(e), "data": []}


def run(*args):
    if len(args) < 1:
        print("Uso: --script-args puntos|lineas|poligonos [id]")
        return

    tabla = args[0].lower()
    id_val = int(args[1]) if len(args) > 1 else 1

    if tabla == "puntos":
        data = {
            "id": id_val,
            "tipo": "Papelera Solar",
            "estado": "Excelente",
            "material": "Metal",
            "codigo_inventario": "PT001",
            "observacion": "Punto actualizado",
            "geom": "POINT(25 25)",
        }
        print(update_punto(data))
    elif tabla == "lineas":
        data = {
            "id": id_val,
            "tipo_via": "Ciclovia",
            "pavimento": "Hormigon",
            "accesible": True,
            "codigo_tramo": "TR001",
            "observacion": "Linea actualizada",
            "geom": "LINESTRING(12 12, 22 22, 35 28)",
        }
        print(update_linea(data))
    elif tabla == "poligonos":
        data = {
            "id": id_val,
            "nombre": "Edificio A Mod",
            "uso_principal": "Investigacion",
            "pisos": 4,
            "estado": "Activo",
            "observacion": "Poligono actualizado",
            "geom": "POLYGON((0 0, 120 0, 120 100, 0 100, 0 0))",
        }
        print(update_poligono(data))
    else:
        print("Tabla no valida")
