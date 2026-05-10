from django.contrib.gis.geos import GEOSGeometry 
from django.forms.models import model_to_dict
from django.db import connection

from buildings2.models import Buildings
from scripts.p1.myLib import p1Settings

from djangoapi.settings import EPSG_FOR_GEOMETRIES, ST_SNAP_PRECISION

def insert(d:dict):
    #create the geometry with geos
    g=GEOSGeometry(d['geom'], srid=p1Settings.EPSG_CODE)
    #print the representation of the object
    if g.valid:
        print("Geometría válida")
    else:
        return {'ok': False, 'message':'Invalid geometry', 'data': None}
    print(g)
    #create a building object, from the model Buildings
    b=Buildings(description=d['description'], area=g.area, perimeter=g.length, height=d['height'], geom=g)
    
    #saves it into the database
    b.save()
    #prints the asigned id of the object in the database
    print(b.id)

    ##################################
    #another way to create the object with a dictionary

    d['geom']=g
    d['area']=g.area
    d['perimeter']=g.length

    #use the ** operator over a dictionary to automatically get the 
    #   fieldname=fieldvalue parameters from the dictionary
    b2=Buildings(**d)
    b2.save()
    print(b2.id)
    return {'ok': True, 'message':'Building inserted', 'data': [{'id':b.id}]}

def insert2(d:dict):
    g=GEOSGeometry(d['geom'], srid=ST_SNAP_PRECISION)
    if g.valid:
        print("Geometría válida")
    else:
        return {'ok': False, 'message':'Invalid geometry', 'data': None}
    d['geom']=g
    b=Buildings(**d)
    b.save()
    d=model_to_dict(b)
    d['geom']=g.wkt
    d['data_creation']=d['data_creation'].strftime("%Y-%m-%d %H:%M:%S")
    return {'ok': True, 'message':'Building inserted', 'data': [d]}


def insert3(d:dict):
    #we first get the snapped wkb format for the geometry:
    cur=connection.cursor()
    query="select st_snaptogrid(st_geomfromtext(%s, %s),%s)"
    cur.execute(query, [d['geom'],EPSG_FOR_GEOMETRIES, ST_SNAP_PRECISION])
    snapped_wkb_geometry=cur.fetchall()[0][0]

    print(f'snapped_wkb_geometry: {snapped_wkb_geometry}')

    #now we can check if it is valid as before:
    g=GEOSGeometry(snapped_wkb_geometry, srid=EPSG_FOR_GEOMETRIES)
    if g.valid:
        print("Geometría válida")
    else:
        return {'ok': False, 'message':'Invalid geometry', 'data': None}
    
    #Now we can check if it intersects with another geomtry in the same layer
    #check if the geometry intersects any existing building
    query=""" 
        select id from buildings2_buildings where ST_relate(
            geom,
            %s,
            'T********'
        )
    """
    cur.execute(query, [snapped_wkb_geometry])
    r=cur.fetchall()

    if len(r)>0:
        return {'ok': False, 'message':'The geometry interior intersects with the following geometries id', 'data': r}

    d['geom']=g
    b=Buildings(**d)
    b.save()
    d=model_to_dict(b)
    d['geom']=g.wkt
    d['data_creation']=d['data_creation'].strftime("%Y-%m-%d %H:%M:%S")
    return {'ok': True, 'message':'Building inserted', 'data': [d]}

def run():
    d_of_values= {
        'description':'Edificio 1', 
        'height':100, 
        'area':2000,
        'geom':'POLYGON((0 0, 10 0, 10 10, 0 11, 0 0))'
    }
    
    print(insert3(d_of_values))

