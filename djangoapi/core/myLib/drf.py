from rest_framework.views import exception_handler
from rest_framework.exceptions import ValidationError, PermissionDenied, NotAuthenticated
from rest_framework.response import Response

from django.contrib.auth.models import User

from core.myLib import generalModule

def manageSerializerErrors(serializerErrorsDict:dict, eventsDictToAdd:dict=None)->dict:
    """
    Recibe el diccionario serializer.errors, que puede tener listas o no en los valores.
    Devuelve un diccionario con los mismos errores, pero sin listas en los valores.
    Si eventsDictToAdd es distinto de None, añade las nuevas claves generadas a este diccionario.
    Crea claves nuevas en el diccionario devuelto que no se repiten para los errores que tenían listas con varios elementos.
    
    Ejemplo:
        serializerErrorsDict = {
            'field1': ['error1'],
            'field2': ['error2-1', 'error2-2'],
        }
    Devuelve:
        {
            'field1': 'error1',
            'field2_xdjfmk': 'error2-1',
            'field2_abcd12': 'error2-2',
        }
    """

    newEventsDict={}
    for event_code, event in serializerErrorsDict.items():
        if isinstance(event,list):
            for m in event:
                if eventsDictToAdd is not None:
                        if event_code in eventsDictToAdd.keys() or event_code in newEventsDict.keys():
                            keyForMessagesDict= event_code + '_' + generalModule.get_random_string(6)
                        else:
                            keyForMessagesDict = event_code
                else :
                        if event_code in newEventsDict.keys():
                            keyForMessagesDict= event_code + '_' + generalModule.get_random_string(6)
                        else:
                            keyForMessagesDict = event_code
                newEventsDict[keyForMessagesDict]=m
        else:
            if eventsDictToAdd is not None:
                if event_code in eventsDictToAdd.keys() or event_code in newEventsDict.keys():
                        keyForMessagesDict= event_code + '_' + generalModule.get_random_string(6)
                else:
                        keyForMessagesDict = event_code
            else :
                if event_code in newEventsDict.keys():
                        keyForMessagesDict= event_code + '_' + generalModule.get_random_string(6)
                else:
                        keyForMessagesDict = event_code
            newEventsDict[keyForMessagesDict]=event
    if eventsDictToAdd:
        return {**eventsDictToAdd, **newEventsDict}
    else:
        return newEventsDict

def custom_exception_handler(exc, context):
    # Obtener la respuesta estándar de DRF
    response = exception_handler(exc, context)

    if response is not None:
        custom_data = {
            "messages": {},
            "access_policy": {},
            "data": []
        }

        # CASO 1: Errores de Validación (400 Bad Request)
        if isinstance(exc, ValidationError):
            custom_data["messages"] =  manageSerializerErrors(response.data, {"request_error": "Invalid data."})
            custom_data["data"] = response.data  # Aquí van los detalles de qué campos fallaron
            custom_data["access_policy"] = {"access": "Acces granted"}

        # CASO 2: Errores de Permisos (401)
        elif isinstance(exc, (PermissionDenied,)):
            # Si ya definiste un mensaje en la política, lo usamos; si no, ponemos uno genérico
            if isinstance(response.data, dict) and "access_policy" in response.data:
                return response # Ya viene formateado desde la política
            
            custom_data["messages"] = {"request_error": "Permission denied."}
            custom_data["access_policy"] = manageSerializerErrors({"request_error": str(exc.detail)})
            custom_data['data']=[]

        # CASO 3: Errores de Autenticación (403)
        elif isinstance(exc, (NotAuthenticated,)):
            # Si ya definiste un mensaje en la política, lo usamos; si no, ponemos uno genérico
            if isinstance(response.data, dict) and "access_policy" in response.data:
                return response # Ya viene formateado desde la política
            
            custom_data["messages"] = {"request_error": "You are not authenticated."}
            custom_data["access_policy"] = manageSerializerErrors({"error": str(exc.detail)})
            custom_data['data']=[]

        # CASO 4: Cualquier otro error de DRF (404, 405, etc.)
        else:
            custom_data["messages"] = manageSerializerErrors(response.data, {"request_error": "Unexpected error."})
            custom_data["data"] = []
            custom_data["access_policy"] = {"access": "Denied"}
        response.data = custom_data
    return response