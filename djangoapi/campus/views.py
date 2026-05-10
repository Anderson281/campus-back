# campus/views.py
# Capa web de la app campus.
# Recibe peticiones HTTP y llama a las funciones ya probadas en djcampus.

import json
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from campus.models import Punto, Linea, Poligono
from scripts.p1.djcampus.insertdj import insert_punto, insert_linea, insert_poligono
from scripts.p1.djcampus.selectdj import select_data
from scripts.p1.djcampus.updatedj import update_punto, update_linea, update_poligono
from scripts.p1.djcampus.deletedj import delete_data


MODELOS = {
    "puntos": Punto,
    "lineas": Linea,
    "poligonos": Poligono,
}

INSERTS = {
    "puntos": insert_punto,
    "lineas": insert_linea,
    "poligonos": insert_poligono,
}

UPDATES = {
    "puntos": update_punto,
    "lineas": update_linea,
    "poligonos": update_poligono,
}


def get_request_data(request):
    # Permite enviar datos como JSON o como form-data/x-www-form-urlencoded.
    if request.content_type and request.content_type.startswith("application/json"):
        try:
            return json.loads(request.body.decode("utf-8"))
        except Exception:
            return {}
    return request.POST.dict()


def normalizar_datos(tabla, data):
    # Ajusta tipos que suelen llegar como texto desde Postman o formularios.
    if tabla == "lineas" and "accesible" in data:
        data["accesible"] = str(data["accesible"]).lower() in ["true", "1", "si", "sí", "yes"]

    if tabla == "poligonos" and "pisos" in data:
        if data["pisos"] not in [None, ""]:
            data["pisos"] = int(data["pisos"])

    return data


@method_decorator(csrf_exempt, name="dispatch")
class HelloCampus(View):
    def get(self, request):
        return JsonResponse({
            "ok": True,
            "message": "Campus. Hello world",
            "data": [request.GET.dict()],
        })

    def post(self, request):
        return JsonResponse({
            "ok": True,
            "message": "Campus. Hello world",
            "data": [get_request_data(request)],
        })


@method_decorator(csrf_exempt, name="dispatch")
class CampusView(View):
    def get(self, request, tabla, accion, id=None):
        if tabla not in MODELOS:
            return JsonResponse({"ok": False, "message": "Tabla no valida", "data": []}, status=400)

        if accion != "select":
            return JsonResponse({"ok": False, "message": "Accion GET no valida. Usa select.", "data": []}, status=400)

        id_value = id if id is not None else 0
        resultado = select_data(MODELOS[tabla], id_value)
        return JsonResponse(resultado)

    def post(self, request, tabla, accion, id=None):
        if tabla not in MODELOS:
            return JsonResponse({"ok": False, "message": "Tabla no valida", "data": []}, status=400)

        data = normalizar_datos(tabla, get_request_data(request))

        if accion == "insert":
            resultado = INSERTS[tabla](data)
            return JsonResponse(resultado)

        if accion == "update":
            if id is None:
                return JsonResponse({"ok": False, "message": "Falta id en la URL", "data": []}, status=400)
            data["id"] = id
            resultado = UPDATES[tabla](data)
            return JsonResponse(resultado)

        if accion == "delete":
            if id is None:
                return JsonResponse({"ok": False, "message": "Falta id en la URL", "data": []}, status=400)
            resultado = delete_data(MODELOS[tabla], id)
            return JsonResponse(resultado)

        return JsonResponse({"ok": False, "message": "Accion POST no valida", "data": []}, status=400)

class HelloWorld(View):
    def get(self, request):
        return JsonResponse({
            "ok": True,
            "message": "Hello world",
            "data": []
        })