from core.myLib.geometryTools import WkbConversor, GeometryChecks

pointWkt= 'POINT(751834.412 4303759.869)'

conv=WkbConversor()
conv.set_wkb_from_wkt(pointWkt)

gc=GeometryChecks(conv.get_as_wkb())

ids=gc.check_st_condition('buildings_buildings','st_contains')
print(gc.get_relate_message())


