# Create your views here.
#Django imports
from django.http import JsonResponse
from django.views import View

from core.myLib.geometryTools import WkbConversor, GeometryChecks
from core.myLib.baseDjangoView import BaseDjangoView
#my code
from buildings2.operations.insertDjango import insert3
from buildings2.operations.deleteDjango import delete
from buildings2.operations.selectDjango import select, selectall
from buildings2.operations.updateDjango import update

class HelloBuildings2(View):
    def get(self, request):
        return JsonResponse({"ok":True,"message": "Buildings. Hello world", "data":[request.GET.dict()]})
    def post(self, request):
        return JsonResponse({"ok":True,"message": "Buildings. Hello world", "data":[request.POST.dict()]})

class Buildings2Insert(View):
    def post(self, request):
        d=request.POST.dict()
        r=insert3(d)
        return JsonResponse(r)

class Buildings2Delete(View):
    def post(self, request):
        d=request.POST.dict()
        r=delete(d)
        return JsonResponse(r)
    
class Buildings2View(BaseDjangoView, ):
    #GET OPERATIONS
    def selectone(self, id):
        r=select({'id':id})
        return JsonResponse(r)

    def selectall(self):
        r=selectall()
        return JsonResponse(r)

    #POST OPERATIONS
    def insert(self, request):
        d=request.POST.dict()
        r=insert3(d)
        return JsonResponse(r)
    def update(self, request, id):
        r=update(request.POST.dict())
        return JsonResponse(r)
    def delete(self, id):
        d={'id':id}
        r=delete(d)
        return JsonResponse(r)
