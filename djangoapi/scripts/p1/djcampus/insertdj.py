# scripts/p1/djcampus/insertdj.py
# Inserciones con Django ORM + validaciones espaciales en PostGIS.
# Se ejecuta con: python manage.py runscript scripts.p1.djcampus.insertdj --script-args poligonos

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
    # PostGIS redondea la geometria. Luego Django la recibe como GEOSGeometry.
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
    # model_to_dict no devuelve la geometria como texto WKT; por eso la convertimos.
    d = model_to_dict(obj)
    d["geom"] = obj.geom.wkt
    return d


def insert_punto(d):
    try:
        g = snap_geom(d["geom"])
        if not g.valid:
            return {"ok": False, "message": "Geometria de punto invalida", "data": []}

        # El punto debe estar dentro de un poligono existente.
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

        obj = Punto(
            tipo=d["tipo"],
            estado=d["estado"],
            material=d.get("material"),
            codigo_inventario=d["codigo_inventario"],
            observacion=d.get("observacion"),
            geom=g,
        )
        obj.save()
        return {"ok": True, "message": "Punto insertado", "data": [model_to_dict_with_geom(obj)]}
    except Exception as e:
        return {"ok": False, "message": str(e), "data": []}


def insert_linea(d):
    try:
        g = snap_geom(d["geom"])
        if not g.valid:
            return {"ok": False, "message": "Geometria de linea invalida", "data": []}

        # Evita cruces reales con otras lineas.
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
            """,
            [d["geom"], EPSG_CODE, SNAP_DISTANCE],
        )
        rows = cur.fetchall()
        if len(rows) > 0:
            return {"ok": False, "message": "La linea se interseca con otra linea", "data": rows}

        obj = Linea(
            tipo_via=d["tipo_via"],
            pavimento=d.get("pavimento"),
            accesible=parse_bool(d.get("accesible", True)),
            codigo_tramo=d["codigo_tramo"],
            observacion=d.get("observacion"),
            geom=g,
        )
        obj.save()
        return {"ok": True, "message": "Linea insertada", "data": [model_to_dict_with_geom(obj)]}
    except Exception as e:
        return {"ok": False, "message": str(e), "data": []}


def insert_poligono(d):
    try:
        g = snap_geom(d["geom"])
        if not g.valid:
            return {"ok": False, "message": "Geometria de poligono invalida", "data": []}

        # Evita cruces reales con otros poligonos.
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
            """,
            [d["geom"], EPSG_CODE, SNAP_DISTANCE],
        )
        rows = cur.fetchall()
        if len(rows) > 0:
            return {"ok": False, "message": "El poligono se interseca con otro poligono", "data": rows}

        obj = Poligono(
            nombre=d["nombre"],
            uso_principal=d.get("uso_principal"),
            pisos=int(d["pisos"]) if d.get("pisos") not in [None, ""] else None,
            estado=d.get("estado"),
            observacion=d.get("observacion"),
            geom=g,
        )
        obj.save()
        return {"ok": True, "message": "Poligono insertado", "data": [model_to_dict_with_geom(obj)]}
    except Exception as e:
        return {"ok": False, "message": str(e), "data": []}


def run(*args):
    if len(args) < 1:
        print("Uso: --script-args puntos|lineas|poligonos")
        return

    tabla = args[0].lower()

    if tabla == "poligonos":
        data = {
            "nombre": "Edificio A",
            "uso_principal": "Docencia",
            "pisos": 3,
            "estado": "Activo",
            "observacion": "Poligono de prueba",
            "geom": "POLYGON((0 0, 100 0, 100 100, 0 100, 0 0))",
        }
        print(insert_poligono(data))
    elif tabla == "puntos":
        data = {
            "tipo": "Papelera",
            "estado": "Bueno",
            "material": "Metal",
            "codigo_inventario": "PT001",
            "observacion": "Punto de prueba",
            "geom": "POINT(20 20)",
        }
        print(insert_punto(data))
    elif tabla == "lineas":
        data = {
            "tipo_via": "Camino",
            "pavimento": "Asfalto",
            "accesible": True,
            "codigo_tramo": "TR001",
            "observacion": "Linea de prueba",
            "geom": "LINESTRING(10 10, 20 20, 30 25)",
        }
        print(insert_linea(data))
    else:
        print("Tabla no valida")
