#Django imports
from django.http import JsonResponse
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
import random, time

"""
Código	Nombre	Uso típico
200	OK	Petición exitosa (valor por defecto).
201	Created	Se ha creado un recurso (ej. un nuevo usuario).
400	Bad Request	Datos enviados inválidos o mal formateados.
401	Unauthorized	El usuario no está autenticado.
403	Forbidden	Autenticado, pero sin permisos para esa acción.
404	Not Found	El recurso solicitado no existe.
500	Internal Server Error	Error inesperado en tu código Python.

"""

def custom_logout_view(request):
    logout(request)
    return redirect("/accounts/login/")  # O a donde desees redirigir después del logout

def notLoggedIn(request):
    return JsonResponse({"ok":False,"message": "You are not logged in", "data":[]},status=400)

class HelloWord(View):
    def get(self, request):
        return JsonResponse({"ok":True,"message": "Core. Hello world. Method GET", "data":[request.GET.dict()]},status=200)
    def post(self,request):
        print(request.POST.get('area','Nada'))
        return JsonResponse({"ok":True,"message": "Core. Hello world. Method POST", "data":[request.POST.dict()]},status=200)

class LoginView(View):
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            username=request.user.username
            return JsonResponse({"ok":True,"message": "The user {0} already is authenticated".format(username), "data":[{'username':request.user.username}]}, status=200)

        username=request.POST.get('username')
        password=request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request,user)#introduce into the request cookies the session_id,
                    # and in the auth_sessions the session data. This way, 
                    # in followoing requests, know who is the user and if
                    # he is already authenticated. 
                    # The coockies are sent in the response header on POST requests
            return JsonResponse({"ok":True,"message": "User {0} logged in".format(username), "data":[{"username": username}]}, status=200)
        else:
            # To make thinks difficult to hackers, you make a random delay,
            # between 0 and 1 second
            seconds=random.uniform(0, 1)
            time.sleep(seconds)
            return JsonResponse({"ok":False,"message": "Wrong user or password", "data":[]},status=400)

class LogoutView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        username=request.user.username
        logout(request) #removes from the header of the request
                            #the the session_id, stored in a cookie
        return JsonResponse({"ok":True,"message": "The user {0} is now logged out".format(username), "data":[]}, status=200)

class IsLoggedIn(View):
    def post(self, request, *args, **kwargs):
        print(request.user.username)
        print(request.user.is_authenticated)
        if request.user.is_authenticated:
            return JsonResponse({"ok":True,"message": "You are authenticated", "data":[{'username':request.user.username}]}, status=200)
        else:
            return JsonResponse({"ok":False,"message": "You are not authenticated", "data":[]}, status=400)
