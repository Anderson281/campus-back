"""
This files can be executed in the following way:

    python manage.py runscript script_without_extension

The scripts must be in the folder scripts

You can pass parameters to the scritp in the following way:+

    python manage.py runscript mainDjango --script-args nombreTabla funcion

All parameters are received in string format

"""
import sys
from scripts.p1.buildingsDjangoModels.insertDjango import insert3

def run(*args):
    """python manage.py runscript scripts.p1.mainDjango --script-args tabla operacion"""
    print(__file__)
    print("Hello script")

    if len(args) == 2:
        tableName = args[0]
        functionName = args[1]     
    else:
        print("Error: You mus give two parameters tableName and functionName to execute the addecuate function.")
        sys.exit(0)


    if tableName not in ["buildings", "trees", "water"]:
        print("Error: The available table names are buildings, trees, water")
        sys.exit(0)
    
    if functionName not in ["insert", "select", "selectAsDict", "update", "delete"]:
        print("Error the available function names are insert, select, delete or update")
        sys.exit(0)

    if tableName == "buildings":
        if functionName=="insert":
            d_of_values= {
                'description':'Edificio 1', 
                'height':100, 
                'area':2000,
                'geom':'POLYGON((0 0, 10 0, 10 10, 0 11, 0 0))'
            }
            print(insert3(d_of_values))
        elif functionName=="select":
            pass
        elif functionName=="selectAsDict":
            pass
        elif functionName=="update":
            pass
        elif functionName=="delete":
            pass
    elif tableName=="trees":
        if functionName=="insert":
            pass
        elif functionName=="select":
            pass
        elif functionName=="update":
            pass
        elif functionName=="delete":
            pass

if __name__ == "__main__":
    main()
