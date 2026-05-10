# scripts/p1/main.py
# Script de prueba para la parte psycopg.
# Se ejecuta desde /usr/src/app/scripts/p1 con:
# python main.py <puntos|lineas|poligonos> <insert|select_tuplas|select_diccionarios|update|delete>

import sys
from psycampus.puntosOOP import PuntosOOP
from psycampus.lineasOOP import LineasOOP
from psycampus.poligonosOOP import PoligonosOOP


def main():
    if len(sys.argv) != 3:
        print("Uso: python main.py <puntos|lineas|poligonos> <insert|select|selectasdict|update|delete>")
        return

    tabla = sys.argv[1].lower()
    accion = sys.argv[2].lower()

    if accion not in ["insert", "select", "selectasdict", "update", "delete"]:
        print("Accion no valida")
        return

    if tabla == "poligonos":
        obj = PoligonosOOP()
        data_insert = {
            "nombre": "Edificio A",
            "uso_principal": "Docencia",
            "pisos": 3,
            "estado": "Activo",
            "observacion": "Poligono de prueba",
            "geom": "POLYGON((0 0, 100 0, 100 100, 0 100, 0 0))",
        }
        data_update = {
            "id": 1,
            "nombre": "Edificio A Mod",
            "uso_principal": "Investigacion",
            "pisos": 4,
            "estado": "Activo",
            "observacion": "Poligono actualizado",
            "geom": "POLYGON((0 0, 120 0, 120 100, 0 100, 0 0))",
        }
    elif tabla == "puntos":
        obj = PuntosOOP()
        data_insert = {
            "tipo": "Papelera",
            "estado": "Bueno",
            "material": "Metal",
            "codigo_inventario": "PT001",
            "observacion": "Punto de prueba",
            "geom": "POINT(20 20)",
        }
        data_update = {
            "id": 1,
            "tipo": "Papelera Solar",
            "estado": "Excelente",
            "material": "Metal",
            "codigo_inventario": "PT001",
            "observacion": "Punto actualizado",
            "geom": "POINT(25 25)",
        }
    elif tabla == "lineas":
        obj = LineasOOP()
        data_insert = {
            "tipo_via": "Camino",
            "pavimento": "Asfalto",
            "accesible": True,
            "codigo_tramo": "TR001",
            "observacion": "Linea de prueba",
            "geom": "LINESTRING(10 10, 20 20, 30 25)",
        }
        data_update = {
            "id": 1,
            "tipo_via": "Ciclovia",
            "pavimento": "Hormigon",
            "accesible": True,
            "codigo_tramo": "TR001",
            "observacion": "Linea actualizada",
            "geom": "LINESTRING(12 12, 22 22, 35 28)",
        }
    else:
        print("Tabla no valida")
        return

    data_select = {"id": 0}
    data_delete = {"id": 1}

    if accion == "insert":
        print(obj.insert(data_insert))
    elif accion == "select":
        print(obj.select(data_select))
    elif accion == "selectasdict":
        print(obj.selectasDict(data_select))
    elif accion == "update":
        print(obj.update(data_update))
    elif accion == "delete":
        print(obj.delete(data_delete))


if __name__ == "__main__":
    main()
