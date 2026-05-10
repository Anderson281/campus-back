from buildings.models import Buildings
#Uso de los modelos para editar

def insertar():
    #cómo insertar
    print('Insertando')
    b=Buildings()
    b.description='hhhh'
    b.geom="POLYGON((0 0, 10 0, 10 10, 0 10, 0 0))"
    b.save()
    print("Insertado", b)

def insertarCondiccionario(d):
    b=Buildings(**d)# el operador **d extrae claves y valores
    b.save()
    print('insertarCondiccionario')
    print(b)

def editar(id):
    #Hay que saber filtrar con los modelos de django: https://www.w3schools.com/django/django_queryset_filter.php
    b=list(Buildings.objects.all().filter(id=id))[0]#esto se llaman lookups
    b.description="gggg"
    b.save()
    print('Salvado', b)

insertar()
insertarCondiccionario({"description":'diccionario', 'geom': "POLYGON((0 0, 10 0, 10 10, 0 10, 0 0))"})
editar(1)