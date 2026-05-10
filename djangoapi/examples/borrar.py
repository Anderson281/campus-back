from enum import Enum
class GeometryFormat(Enum):
    WKT = 1
    GEOJSON = 2
    WKB = 3

def a(a:int):
    print(a)

a(GeometryFormat.WKT.value)