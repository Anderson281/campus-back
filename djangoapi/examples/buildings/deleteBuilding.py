from djangoapi.buildings.models import Buildings
filterById = Buildings.objects.filter(id=1)

#all the results are querysets: https://docs.djangoproject.com/en/5.1/ref/models/querysets/
#to access to the results you can convert the queryset to a list
l=list(filterById)
print(l)

p=l[0]

print(p.id)
print(p.area)
print(p.geom)

p.delete()