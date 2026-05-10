from myLib.connect import connect
from myLib.p1Settings import EPSG_CODE

def update():
    conn=connect()
    cur=conn.cursor()
    cons="""
        UPDATE
            d.buildings 
        SET 
            (description, area, geom) = ROW(%s, %s, st_geometryFromText(%s,%s))    
        WHERE
            id>%s
        """
    # As there are 5 %s, you need a list with 5 values: 
    #   [description, area, the_geom_wkt, the_epsg_code, 
    #           the_id_to_select_the_row]
    valuesList=['New description',200,'POLYGON((0 0, 10 0, 10 10, 0 10, 0 0))',EPSG_CODE, 6]
    cur.execute(cons, valuesList)
    print(cur.rowcount)
    conn.commit()
    cur.close()
    conn.close()
    print("Updated")


