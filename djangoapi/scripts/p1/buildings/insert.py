from myLib.connect import connect
from myLib.p1Settings import EPSG_CODE

def insert():
    conn=connect()
    cur=conn.cursor()
    cons="""
        INSERT INTO d.buildings 
            (description, area,geom)
        VALUES
            (%s,%s,
            st_geometryFromText(%s,%s))
        RETURNING id
        """
    cur.execute(cons,
                ['My first building',
                 100,
                 'POLYGON((0 0, 100 0, 100 100, 0 100, 0 0))',
                 EPSG_CODE
                 ])
    conn.commit()
    l=cur.fetchall()
    #print(cur.fetchall()[0][0]) <-- ERROR. YOU ONLY CAN FECTH THE RESULTS ONCE
    print(l)
    print(l[0][0])
    cur.close()
    conn.close()
    print("Inserted")


