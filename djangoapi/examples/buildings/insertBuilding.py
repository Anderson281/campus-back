from django.contrib.gis.geos import GEOSGeometry
from djangoapi.buildings.models import Buildings

#create the geometry with geos
g=GEOSGeometry('POLYGON((0 0, 10 0, 10 10, 0 11, 0 0))', srid=25830)
#print the representation of the object
print(g)

#create a building object, from the model Buildings
b=Buildings(description='Edificio 1', area=100, geom=g)
#saves it into the database
b.save()

#prints the asigned id of the object in the database
print(b.id)

#another way to create the object with a dictionary
d_of_values= {'description':'Edificio 1', 'area':g.area, 'geom':g}
#you need to use the ** to unpack the dictionary
b=Buildings(**d_of_values)
b.save()
print(b.id)



