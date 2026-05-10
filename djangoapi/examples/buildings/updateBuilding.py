from djangoapi.buildings.models import Buildings
from django.contrib.gis.geos import GEOSGeometry

#using django lookups https://docs.djangoproject.com/en/5.1/ref/models/lookups/
#using spatila lookups
#https://docs.djangoproject.com/en/5.1/ref/contrib/gis/geoquerysets/#std-fieldlookup-contains_properly
#using geodjango lookups 
# Filtrar edificios con área menor que 100 (less than --> lt, greater than --> gt)

filterById = Buildings.objects.filter(id=1)

#all the results are querysets: https://docs.djangoproject.com/en/5.1/ref/models/querysets/
#to access to the results you can convert the queryset to a list
l=list(filterById)
print(l)

p=l[0]

print(p.id)
print(p.area)
print(p.geom)

p.area=800
p.description='Edificio 1'
p.save()

print(p.description)



