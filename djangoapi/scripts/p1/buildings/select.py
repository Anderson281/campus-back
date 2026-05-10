from myLib.connect import connect
from psycopg.rows import dict_row


def select(asDict=False):
    conn=connect()

    if asDict:
        #The rows are dicts
        cur=conn.cursor(row_factory=dict_row)
    else:
        #Te rows are tuples
        cur=conn.cursor()

    cons="""
        SELECT 
            id, description, area, st_astext(geom)
        FROM 
            d.buildings 
        WHERE
            id>%s
        """
    cur.execute(cons, [0])
    l=cur.fetchall()
    print(l)
    print('First row:')
    print(l[0])
    conn.commit()
    cur.close()
    conn.close()
    print("Selected")


