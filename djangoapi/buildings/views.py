# Create your views here.
#Django imports
from django.http import JsonResponse
from django.views import View
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.forms.models import model_to_dict
from django.contrib.auth.mixins import LoginRequiredMixin

#Geoss
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.db.models.functions import SnapToGrid


#rest_framework imports
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response

#My imports
from core.myLib.geometryTools import WkbConversor, GeometryChecks
from buildings.models import Buildings, Owners, BuildingsOwners
from buildings.serializers import BuildingsSerializer, OwnersSerializer, BuildingsOwnersSerializer
from djangoapi.settings import EPSG_FOR_GEOMETRIES, ST_SNAP_PRECISION, MAX_NUMBER_OF_RETRIEVED_ROWS
from core.myLib.baseDjangoView import BaseDjangoView

def custom_logout_view(request):
    logout(request)
    return redirect("/accounts/login/")  # O a donde desees redirigir después del logout

class HelloWord(View):
    def get(self, request):
        return JsonResponse({"ok":True,"message": "Buildings. Hello world", "data":[]})

class BuildigsView(LoginRequiredMixin, BaseDjangoView):
    """

    The get and post methods are defined in the BaseDjangoView. They forward the request
    to the methods selectone, selectall, insert, update, and delete, depending of the 
    action parameter in the URL.

    This class redefine the the methods selectone, selectall, insert, update, and delete
    of the BaseDjangoView class to add a new action, insert2.
  
    To use this view:
    To get a record, the URL must be like:
        GET /buildings_view/selectone/<id>/
    To get all the records, the URL must be like:
        GET /buildings_view/selectall/
    To insert a record, the URL must be like:
        POST /buildings_view/insert/ --> The data must be sent in the body of the request.
    To update a record, the URL must be like:
        POST /buildings_view/update/<id>/ --> The data must be sent in the body of the request.
    To delete a record, the URL must be like:
        POST /buildings_view/delete/<id>/
    """
    
    def post(self, request, *args, **kwargs):
        """
        Redefines the post method of the BaseDjangoView class to add a new action.
        If the action is insert2, it will call the insert2 method.
        if not it will call the post method of the BaseDjangoView class.
        """
        action = kwargs.get('action')
        print(f"action child: {action}")

        if action == 'insert2':
            return self.insert2(request)
        else:            
            return super().post(request, *args, **kwargs)

    #GET OPERATIONS
    def selectone(self, id):
        l=list(Buildings.objects.filter(id=id))
        if len(l)==0:
            return JsonResponse({'ok':False, "message": f"The building id {id} does not exist", "data":[]}, status=200)
        b=l[0]
        d=model_to_dict(b)
        d['geom']=b.geom.wkt
        return JsonResponse({'ok':True, 'message': 'Building Retriewed', 'data': [d]}, status=200)

    def selectall(self):
        l=Buildings.objects.all()[:MAX_NUMBER_OF_RETRIEVED_ROWS]
        data=[]
        for b in l:
            d=model_to_dict(b)
            d['geom']=b.geom.wkt
            data.append(d)
        return JsonResponse({'ok':True, 'message': 'Data retrieved', 'data': data}, status=200)

    #POST OPERATIONS
    def insert(self, request):
        """
        Inserts the polygon. Latter snap it to the grid. This must be done
        in the database. So we need to insert it before.
        After the building has been inserted:
            - snap it to grid
            - Check if the geometry is valid
            - Check if the interior intersects with other geometry
            - If any check fails, remove the row.
            - The only inconvenient is the id counter sums one more
        """
        print(f"Insert building")
        print(f"Request: {request.POST}")
        print(f"Request body: {request.body}")
        #Check if the geometry is present
        originalWkt=request.POST.get('geom', None)
        if originalWkt is None:
            return JsonResponse({'ok':False, 'message': 'The geometry is mandartory', 'data':[]}, status=400)
        
        #Creates the geometry
        g=GEOSGeometry(request.POST.get('geom',''), srid=EPSG_FOR_GEOMETRIES)
        #print the representation of the object
        print(f"Original geometry: {g}")

        description = request.POST.get('description','') 
        b=Buildings(description=description, area=g.area, geom=g)
        b.save()
        print(f"Geometry inserted id: {b.id}")

        #Update the geometry to an snaped one yo the grid
        Buildings.objects.filter(id=b.id).update(geom=SnapToGrid('geom', ST_SNAP_PRECISION))

        #Now we get a new object with the new geometry to perform the checks
        b=Buildings.objects.get(id=b.id)
        print('Snapped geometry',b.geom.wkt)
        #bGeos=GEOSGeometry(b.geom.wkt, srid=25830)
        #valid=bGeos.valid
        #b.geom is a GEOSGeometry object, so we can use it directly
        valid=b.geom.valid
        print(f'Valid: {valid}')
        if not valid:
            print(f"Deleting invalid geometry {b.id}")
            b.delete()
            return JsonResponse({'ok':False, 'message': 'The geometry is not valid after the st_SnapToGrid', 'data':[]}, status=200)   

        #create a filter to get all the geometries which interiors intersects,
        #but excluding the one just created
        filt=Buildings.objects.filter(geom__relate=(g.wkt,'T********')).exclude(id=b.id)
        print(f"Query:{filt.query}")
        exist=filt.exists()
        print(f"Exists {exist}") 
        n=filt.count() 
        print(f"Count: {n}")
        print(f"Values: {list(filt)}")
        
        if exist:
            print(f"Deleting de building id {b.id}, as it intersects with others")
            b.delete()
            return JsonResponse({'ok':False, 'message': f'The building intersects with {n} building/s'}, status=200)
        
        #create a building object, from the model Buildings
        d=model_to_dict(b)
        d['geom']=b.geom.wkt
        return JsonResponse({'ok':True, 'message': 'Data inserted', 'data': [d]}, status=201)

    def update(self, request, id):
        """
        On update you shoud also check the new geometry: snap it, check if it is valid,
            check if it intersects with others except itself.
        
        The problem here is, if after having updated the geometry, if it is not valid, 
            or interesects with others, you must restore the original geometry.
            This is perfectry possible but we are not going to do it, istead
            we are going to use a psycop connection and a raw sql query to
            get the snapped geometry as wkb. This demonstrates
            some times it is better to know raw sql.
        """
        l=list(Buildings.objects.filter(id=id))
        if len(l)==0:
            return JsonResponse({'ok':False, "message": f"The building id {id} does not exist", "data":[]}, status=200)
        b=l[0]

        originalWkt=request.POST.get('geom', None)
        
        if originalWkt is not None:
            conversor=WkbConversor()
            wkb=conversor.set_wkt_from_text(originalWkt)
            newWkt=conversor.get_as_wkt()
            geojson=conversor.get_as_geojson()
            gc=GeometryChecks(wkb)
            isValid=gc.is_geometry_valid()
            interesectionIds=gc.check_st_relate('buildings_buildings','T********', id_to_avoid=id)
            thereAre = gc.are_there_related_ids()

            print(f"Snaped wkt: {newWkt}")
            print(f"Snaped geojson: {geojson}")
            print(f"Snaped is valid: {isValid}")
            print(f"Snaped intersection ids: {interesectionIds}")
            print(f"There are intersection ids: {thereAre}")
            print(gc.get_relate_message())

            if not(isValid):
                return JsonResponse({'ok':False, 'message': 'The geometry is not valid after the st_SnapToGrid', 'data':[]}, status=200)   
            if gc.are_there_related_ids():
                return JsonResponse({'ok':False, 'message': gc.get_relate_message(), 'data':gc.related_ids}, status=200)   
            b.geom=wkb
            b.description=request.POST.get('description', '')
            polyGeos=GEOSGeometry(wkb)
            b.area=polyGeos.area
            b.save()
            d=model_to_dict(b)
            d['geom']=conversor.get_as_wkt()#snaped version
        else:
            return JsonResponse({'ok':False, 'message': 'Update. The geometry is mandartory', 'data':[]}, status=200)
        
        return JsonResponse({'ok':True, 'message': "Building updated", 'data':[d]}, status=200)   

    def delete(self, id):
        l=list(Buildings.objects.filter(id=id))
        if len(l)==0:
            return JsonResponse({'ok':False, "message": f"The building id {id} does not exist", "data":[]}, status=200)
        b=l[0]
        b.delete()  
        return JsonResponse({'ok':True, "message": f"The building id {id} has been deleted", "data":[]}, status=200)

    def insert2(self, request):
        """
        This method do the same that the insert methid, 
        but by using the core/mylib/geometryTools.py module. 
        The geometryTools.py has been coded by the teacher,
        and has been created 
        because I realized that using the Geoss library 
        is a bit complicated, overall to update, 
        due to the geometry checks we do.
        """
        originalWkt=request.POST.get('geom', None)
        
        if originalWkt is not None:
            conversor=WkbConversor()
            wkb=conversor.set_wkt_from_text(originalWkt)
            gc=GeometryChecks(wkb)
            isValid=gc.is_geometry_valid()
            gc.check_st_relate('buildings_buildings','T********')
            print(gc.get_relate_message())

            if not(isValid):
                return JsonResponse({'ok':False, 'message': 'The geometry is not valid after the st_SnapToGrid', 'data':[]}, status=400)   
            if gc.are_there_related_ids():
                return JsonResponse({'ok':False, 'message': gc.get_relate_message(), 'data':gc.related_ids}, status=400)   
            
            b=Buildings()
            b.geom=wkb
            b.description=request.POST.get('description', '')
            b.area=b.geom.area
            b.save()
            d=model_to_dict(b)
            d['geom']=b.geom.wkt
        else:
            return JsonResponse({'ok':False, 'message': 'The geometry mandartory', 'data':[]}, status=200)

        return JsonResponse({'ok':True, 'message': "Building Inserted", 'data':[d]}, status=200)   



class BuildingsModelViewSet(viewsets.ModelViewSet):
    """
    DJANGO REST FRAMEWORK VIEWSET.

    The ModelViewSet class is a special view that Django Rest Framework 
        provides to handle the CRUD operations of a model
    
    The actions provided by the ModelViewSet class are:

        -list()  -> GET operation over /buildings/buildings/. It will return all reccords

        -retrieve() ->GET operation over /buildings/buildings/<id>/. 
                    It will return the record with the id.

        -create() -> POST operation over /buildings/buildings/. It will insert a new record

        -update() -> PUT operation over /buildings/buildings/<id>/. 
                    It will update the record with the id.

        -partial_update() -> PATCH operation over /buildings/buildings/<id>/. 
                It will update partially the record with the id.
                The difference between update and partial_update is that the first one
                will update all the fields of the record, while the second one will update
                only the fields that are present in the request.

        -destroy() -> DELETE operation over /buildings/buildings/<id>/. 
                It will delete the record with the id.

    """

    queryset = Buildings.objects.all()
    serializer_class = BuildingsSerializer#The serializer that will be used to serialize 
                            #the data. and check the data that is sent in the request.
    permission_classes = [permissions.AllowAny]#Any can use it.
                                # Use https://rsinger86.github.io/drf-access-policy/
                                # to more advanced permissions management



class OwnersModelViewSet(viewsets.ModelViewSet):
    """
    DJANGO REST FRAMEWORK VIEWSET.

    The ModelViewSet class is a special view that Django Rest Framework 
        provides to handle the CRUD operations of a model
    
    The actions provided by the ModelViewSet class are:
        -list()  -> GET operation over /buildings/owners/. It will return all reccords
        -retrieve() ->GET operation over /buildings/owners/<id>/. 
                    It will return the record with the id.
        -create() -> POST operation over /buildings/owners/. It will insert a new record
        -update() -> PUT operation over /buildings/owners/<id>/. 
                    It will update the record with the id.
        -partial_update() -> PATCH operation over /buildings/owners/<id>/. 
                It will update partially the record with the id.
                The difference between update and partial_update is that the first one
                will update all the fields of the record, while the second one will update
                only the fields that are present in the request.
        -destroy() -> DELETE operation over /buildings/owners/<id>/. 
                It will delete the record with the id.
    """
    queryset = Owners.objects.all()
    serializer_class = OwnersSerializer#The serializer that will be used to serialize 
                            #the data. and check the data that is sent in the request.
    permission_classes = [permissions.AllowAny]#Any can use it.
                                # Use https://rsinger86.github.io/drf-access-policy/
                                # to more advanced permissions management

class BuildingsOwnersModelViewSet(viewsets.ModelViewSet):
    queryset = BuildingsOwners.objects.all()  #<- Vamos a definir una función para delimitar los objetos
    serializer_class = BuildingsOwnersSerializer#The serializer that will be used to serialize 
                            #the data. and check the data that is sent in the request.
    permission_classes = [permissions.AllowAny]#Any can use it.
                                # Use https://rsinger86.github.io/drf-access-policy/
                                # to more advanced permissions management

    def get_queryset(self):
        #IMPORTANTE
        #limitar los registros en los que el usuario autenticado es el propietario
        #user_id=self.request.user.id
        #pero como en estos ejemplos no se requiere autenticación, ponemos el usuario a id=1
        user_id=1
        return BuildingsOwners.objects.all().filter(id=user_id)

    #define custom methods
    #detail=false indicates that it works with all objects
    #and the url must not have the id  ej. /55/ 
    @action(detail=False, methods=['get'])
    def custom_method(self, request, *args, **kwargs):
        objList: list[BuildingsOwners] = list(self.get_queryset())#obtiene una lista de todos las filas
        data=[]
        for obj in objList:
            d={'dni':obj.owner.dni, 'description':obj.building.description}
            data.append(d)
        return Response(data=data)
    
    #define custom methods
    #detail=true indicates that it works only with the object which id is in the url
    #and the url must not have the id  ej. /55/ 
    @action(detail=True, methods=['get'])
    def custom_method_detail(self, request, *args, **kwargs):
        obj:BuildingsOwners = self.get_object()#obtiene el objeto del id en la url (55)
        d={'dni':obj.owner.dni, 'description':obj.building.description}
        return Response(data=[d])