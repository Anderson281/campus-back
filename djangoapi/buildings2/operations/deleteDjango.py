from django.contrib.gis.geos import GEOSGeometry 
from django.forms.models import model_to_dict
from django.db import connection

from buildings2.models import Buildings
from scripts.p1.myLib import p1Settings

from djangoapi.settings import EPSG_FOR_GEOMETRIES, ST_SNAP_PRECISION

def delete(d:dict):
    #create the geometry with geos
    f=Buildings.objects.filter(id=d['id'])
    l=list(f)
    if len(l)<1:
        return {"ok":False, "Message": f"No buildings with the id {d['id']}", "data":None}
    b:Buildings=l[0]
    b.delete()
    return {'ok':True, 'Message': f"Buildings deleted: 1",
            'data':[{'id':d["id"]}]}

    #g=GEOSGeometry(d['geom'], srid=p1Settings.EPSG_CODE)
 
def run():
    d_of_values= {
        'id':1,
        'description':'Edificio 1', 
        'height':100, 
        'area':2000,
        'geom':'POLYGON((0 0, 10 0, 10 10, 0 11, 0 0))'
    }
    
    print(delete(d_of_values))

