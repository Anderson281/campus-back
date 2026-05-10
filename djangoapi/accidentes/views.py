from django.contrib.auth.models import User

#rest_framework imports
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response

from .models import Accidentes
from .serializers import AccidentesSerializer
from .accessPolicy import AccidentesAccessPolicy

class AccidentesModelViewSet(viewsets.ModelViewSet):
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

    queryset = Accidentes.objects.all()
    serializer_class = AccidentesSerializer#The serializer that will be used to serialize 
                            #the data. and check the data that is sent in the request.
    permission_classes = [AccidentesAccessPolicy]#Any can use it.
                                # Use https://rsinger86.github.io/drf-access-policy/
                                # to more advanced permissions management
    def get_queryset(self):
        #IMPORTANTE
        #limitar los registros en los que el usuario autenticado es el propietario
        user: User=self.request.user
        if user.groups.filter(name='admin').exists():
            return Accidentes.objects.all()
        elif user.groups.filter(name='asegurado').exists():
            return Accidentes.objects.all().filter(creator_id=user.id)
        

    # def destroy(self, request, *args, **kwargs):
    #     if not request.user.groups.filter(name='admin').exists():
    #         return Response({'messages':'Usted no puede eliminar accidentes'})
    #     return super().destroy(request, *args, **kwargs)
