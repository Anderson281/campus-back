from psycopg.rows import dict_row

from myLib.connect import connect
from myLib.p1Settings import EPSG_CODE


class BuildingsOOP():
    def __init__(self):
        self.conn=connect()
        self.cur=self.conn.cursor()
    def disconnect(self):
        self.cur.close()
        self.conn.close()
    def insert(self):
        cons="""
        INSERT INTO d.buildings 
            (description, area,geom)
        VALUES
            (%s,%s,
            st_geometryFromText(%s,%s))
        RETURNING id
        """
        self.cur.execute(cons,
                    ['My first building',
                    100,
                    'POLYGON((0 0, 100 0, 100 100, 0 100, 0 0))',
                    EPSG_CODE
                    ])
        self.conn.commit()
        l=self.cur.fetchall()
        #print(cur.fetchall()[0][0]) <-- ERROR. YOU ONLY CAN FECTH THE RESULTS ONCE
        print(l)
        print(l[0][0])
        self.disconnect()
        print("Inserted")
    def select(self, asDict=True):
        if asDict:
            #The rows are dicts
            self.cur=self.conn.cursor(row_factory=dict_row)
        
        cons="""
        SELECT 
            id, description, area, st_astext(geom)
        FROM 
            d.buildings 
        WHERE
            id>%s
        """
        self.cur.execute(cons, [0])
        l=self.cur.fetchall()
        print(l)
        print('First row:')
        print(l[0])
        self.disconnect()
        print("Selected")




            
