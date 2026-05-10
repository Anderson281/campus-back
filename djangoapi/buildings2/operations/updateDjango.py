from django.contrib.gis.geos import GEOSGeometry 
from django.forms.models import model_to_dict
from django.db import connection

from buildings2.models import Buildings
from scripts.p1.myLib import p1Settings

from djangoapi.settings import EPSG_FOR_GEOMETRIES, ST_SNAP_PRECISION

def update(d:dict):
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

    #create the geometry with geos
    f=Buildings.objects.filter(id=d['id'])
    l=list(f)
    if len(l)>0:
        b:Buildings=l[0]
    else:
        return {'ok':False, "Mesage": f"No buildings found with id {d['d'], 'data':None}"}

    b.geom=g
    b.description=d['description']
    b.height=d["height"]
    b.save()
    d=model_to_dict(b)
    d['geom']=g.wkt
    d['data_creation']=d['data_creation'].strftime("%Y-%m-%d %H:%M:%S")

    return {'ok':True, 'Message': f"Updated buildings: {len(l)}",
            'data':[d]}

    #g=GEOSGeometry(d['geom'], srid=p1Settings.EPSG_CODE)
 
def run():
    d_of_values= {
        'id':1,
        'description':'Edificio 222', 
        'height':500, 
        'area':2000,
        'geom':'POLYGON((0 0, 11 0, 10 10, 0 11, 0 0))'
    }
    
    print(update(d_of_values))

