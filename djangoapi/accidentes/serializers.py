
from rest_framework import serializers
from django.contrib.auth import get_user_model

from core.myLib.geoModelSerializer import GeoModelSerializer
from .models import Accidentes
from core.myLib.baseUserSerializer import BaseUserSerializer

class AccidentesSerializer(GeoModelSerializer, BaseUserSerializer):
    check_geometry_is_valid = True #if true ºit will check if the geometry is valid: not self-intersecting and closed
    matrix9IM = 'T********' #matrix 9IM for the relation of the geometries: 'T********' = interiors intersects
    check_st_relation = False #if the new geometry must be checked against 
            #the other geometries in the table according to the matrix9IM. If any geometry
            #has the relation with the new geometry, the new geometry is not saved
            #an a validation error is raised, with the ids of the geometries that have the relation

    class Meta:
        model = Accidentes
        fields = GeoModelSerializer.Meta.fields + ['description', 'creator'] # The serializer 
    
    def validate(self, data):
        data['creator']= self.get_creator_user()
        return data


    