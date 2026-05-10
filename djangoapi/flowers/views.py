from django.views import View
from django.http import JsonResponse
from flowers.models import Flower as FlowerModel
from django.forms.models import model_to_dict
from django.contrib.gis.geos import GEOSGeometry
from djangoapi.settings import EPSG_FOR_GEOMETRIES
from core.myLib.baseDjangoView import BaseDjangoView

class HelloWord(View):
    def get(self, request):
        v1=request.GET.get('v1')
        v2=request.GET.get('v2')
        return JsonResponse({"ok":True,"message": "Buildings. Helloworld. By get", "data":[v1,v2]})
    def post(self, request):
        v1=request.POST.get('v1')
        v2=request.POST.get('v2')
        return JsonResponse({"ok":True,"message": "Buildings. Helloworld. By post", "data":[v1, v2]})


class Flower2(View):
    def get(self, request):
        id=request.GET.get('id')
        print(f'id {id}')
#        f=FlowerModel.objects.get(id=id)
        f=list(FlowerModel.objects.filter(id=id))

        if len(f)<1:
            return JsonResponse({"ok":False,"message": f"The flowe {id} does not exist", "data":[]})
        f=f[0]
        d=model_to_dict(f)
        d['geom']=f.geom.wkt        
        return JsonResponse({"ok":True,"message": "Buildings. Helloworld. By get", "data":[d]})
    
    def post(self, request):
        description=request.POST.get('description')
        health=request.POST.get('health')
        geom=GEOSGeometry(request.POST.get('geom',''), srid=EPSG_FOR_GEOMETRIES)
        age_days=request.POST.get('age_days')
        f=FlowerModel()
        f.age_days=age_days
        f.description=description
        f.heath=health
        f.geom=geom
        f.save()

        return JsonResponse({"ok":True,"message": f"Building inserted. if: {f.id}", "data":[{'id':f.id}]})

class Flower(BaseDjangoView):
    def insert(self, request):
        description=request.POST.get('description')
        health=request.POST.get('health')
        geom=GEOSGeometry(request.POST.get('geom',''), srid=EPSG_FOR_GEOMETRIES)
        age_days=request.POST.get('age_days')
        f=FlowerModel()
        f.age_days=age_days
        f.description=description
        f.heath=health
        f.geom=geom
        f.save()
        return JsonResponse({"ok":True,"message": f"Building inserted. if: {f.id}", "data":[{'id':f.id}]})

    def selectone(self, id):
        print(f'id {id}')
#        f=FlowerModel.objects.get(id=id)
        f=list(FlowerModel.objects.filter(id=id))

        if len(f)<1:
            return JsonResponse({"ok":False,"message": f"The flowe {id} does not exist", "data":[]})
        f=f[0]
        d=model_to_dict(f)
        d['geom']=f.geom.wkt        
        return JsonResponse({"ok":True,"message": "Buildings. Helloworld. By get", "data":[d]})
            
    def selectall(self):
        lf=list(FlowerModel.objects.all())
        if len(lf)<1:
            return JsonResponse({"ok":False,"message": f"No flowers still", "data":[]})
        l=[]
        for f in lf:
            d=model_to_dict(f)
            d['geom']=f.geom.wkt
            l.append(d)     
        return JsonResponse({"ok":True,"message": f"Flowers retriewed {len(lf)}", "data":l})
   
    def update(self, request,id):
        f=list(FlowerModel.objects.filter(id=id))
        if len(f)<1:
            return JsonResponse({"ok":False,"message": f"The flower {id} does not exist", "data":[]})
        f=f[0]
        description=request.POST.get('description')
        health=request.POST.get('health')
        geom=GEOSGeometry(request.POST.get('geom',''), srid=EPSG_FOR_GEOMETRIES)
        age_days=request.POST.get('age_days')
        f.heath=health
        f.geom=geom
        f.age_days=age_days
        f.description=description
        f.save()
        d=model_to_dict(f)
        d['geom']=f.geom.wkt   
        return JsonResponse({"ok":True,"message": f"The flower {id} updated", "data":[d]})

    def delete(self, id):
        f=list(FlowerModel.objects.filter(id=id))
        if len(f)<1:
            return JsonResponse({"ok":False,"message": f"The flower {id} does not exist", "data":[]})
        f=f[0]
        f.delete()
        return JsonResponse({"ok":True,"message": f"The flower {id} has been deleted", "data":[]})

# Create your views here.
