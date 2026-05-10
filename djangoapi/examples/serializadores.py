#Uso de los serializadores

from buildings.serializers import OwnersSerializer, BuildingsSerializer
from buildings.models import Buildings


print('Serializadores: OWNERS')
d={"name": "Gasp"}

s=OwnersSerializer(data=d)
if s.is_valid(raise_exception=False):
    print('Datos válidos')
    s.save()
else:
    print(s.errors)

d={"name": "Gasp", 'dni': '88888'}

s=OwnersSerializer(data=d)
if s.is_valid(raise_exception=False):
    print('Datos válidos')
    s.save()
else:
    print(s.errors)

d={"name": "Gasp", 'dni': '888888888'}

s=OwnersSerializer(data=d)
if s.is_valid(raise_exception=False):
    print('Datos válidos')
    s.save()
else:
    print(s.errors)

print('Serializadores: BUILDINGS')

d={'description':'con el serializador', 'geom': 'POLYGON((0 0, 10 0, 10 10, 0 10, 20 5, 0 0))'}

s=BuildingsSerializer(data=d)
if s.is_valid(raise_exception=False):
    print('Datos válidos 1')
    s.save()
else:
    print('No valido 1', s.errors)



d={'description':'con el serializador2', 'geom': 'POLYGON((0 0, 10 0, 10 10, 0 10, 0 0))'}
s=BuildingsSerializer(data=d)
if s.is_valid(raise_exception=False):
    print('Datos válidos 2')
    s.save()
    print(s.data) #serializa los datos --> a diccionario
else:
    print('No valido 2', s.errors)

#Serializar un objeto:
print('Insertando')
b=Buildings()
b.description='hhhh'
b.geom="POLYGON((0 0, 10 0, 10 10, 0 10, 0 0))"
b.save()

s=BuildingsSerializer(b)#se pasa la instancia directamente
print(s.data) #serializa los datos --> a diccionario
