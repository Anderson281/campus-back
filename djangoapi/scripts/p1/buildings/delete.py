from myLib.connect import connect

def delete():
    conn=connect()
    cur=conn.cursor()
    cons="""
        DELETE FROM
            d.buildings  
        WHERE
            id=%s
        """
    # As there are 5 %s, you need a list with 5 values: 
    #   [description, area, the_geom_wkt, the_epsg_code, 
    #           the_id_to_select_the_row]
    valuesList=[7]
    cur.execute(cons, valuesList)
    print(cur.rowcount)
    conn.commit()
    cur.close()
    conn.close()
    print("Deleted")


