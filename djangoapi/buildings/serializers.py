
from rest_framework import serializers

from core.myLib.geoModelSerializer import GeomodelPolygonSerializer
from .models import Buildings, Owners, BuildingsOwners

class BuildingsSerializer(GeomodelPolygonSerializer):
    check_geometry_is_valid = True #if true ºit will check if the geometry is valid: not self-intersecting and closed
    matrix9IM = 'T********' #matrix 9IM for the relation of the geometries: 'T********' = interiors intersects
    check_st_relation = False #if the new geometry must be checked against 
            #the other geometries in the table according to the matrix9IM. If any geometry
            #has the relation with the new geometry, the new geometry is not saved
            #an a validation error is raised, with the ids of the geometries that have the relation

    class Meta:
        model = Buildings
        fields = GeomodelPolygonSerializer.Meta.fields + ['description'] # The serializer 
                    #assumes that the model has the geometry field \textit{geom}. 
                    # add here the rest of the fields of the model that you want to serialize
                    # and that are not in the GeoModelSerializer

    def validate_geom(self, value):
        """Validates if a geometry is valid.
            Do not do anythin special. Simple is an example of how to override the father method
        """
        print('validate_geom, child')
        return super().validate_geom(value)
        
class OwnersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owners
        fields = ['id', 'name', 'dni']
    
    #you can validate the fields of the model using the validate_<field_name> method
    #def validate_<field_name>(self, value):
    def validate_name(self, value):
        if 'bad' in value:
            raise serializers.ValidationError("The name can't contain 'bad'.")
        return value
    
class BuildingsOwnersSerializer(serializers.ModelSerializer):
    building_description = serializers.SerializerMethodField()  # Este campo es para serialización (output)
    owner_dni = serializers.SerializerMethodField()  # Este campo es para serialización (output)
    class Meta:
        model = BuildingsOwners
        fields = ['id', 'building', 'owner', 'owner_percentage', 'building_description', 'owner_dni']

    def get_building_description(self, obj:BuildingsOwners):
        return obj.building.description

    def get_owner_dni(self, obj:BuildingsOwners):
        return obj.owner.dni

    def validate_owner_percentage(self, value):
        print('validate_owner_percentage', value)
        if value <=0 or value > 100:
            raise serializers.ValidationError({'owner_percentage': 'From the serializer. The owner_percentage must be between 0 and 100'})
            pass
        return value
    