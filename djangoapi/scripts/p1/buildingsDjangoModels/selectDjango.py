from django.contrib.gis.geos import GEOSGeometry 
from django.forms.models import model_to_dict
from django.db import connection

from buildings2.models import Buildings
from scripts.p1.myLib import p1Settings

from djangoapi.settings import EPSG_FOR_GEOMETRIES, ST_SNAP_PRECISION

def select(d:dict):
    #create the geometry with geos
    f=Buildings.objects.filter(id=d['id'])
    l=list(f)
    b:Buildings=l[0]
    d=model_to_dict(b)
    g=GEOSGeometry(d['geom'], srid=EPSG_FOR_GEOMETRIES)
    d['geom']=g.wkt
    d['data_creation']=d['data_creation'].strftime("%Y-%m-%d %H:%M:%S")
    return {'ok':True, 'Message': f"Retriewed buildings: {len(l)}",
            'data':[d]}

    #g=GEOSGeometry(d['geom'], srid=p1Settings.EPSG_CODE)
 
def run():
    d_of_values= {
        'id':1,
        'description':'Edificio 1', 
        'height':100, 
        'area':2000,
        'geom':'POLYGON((0 0, 10 0, 10 10, 0 11, 0 0))'
    }
    
    print(select(d_of_values))

