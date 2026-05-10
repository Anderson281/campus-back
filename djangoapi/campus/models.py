# campus/models.py
# Modelos Django para las tres capas espaciales.
# Django usara estos modelos para crear o leer las tablas de proyecto_desweb.

from django.contrib.gis.db import models


class Punto(models.Model):
    tipo = models.CharField(max_length=50)
    estado = models.CharField(max_length=50)
    material = models.CharField(max_length=50, blank=True, null=True)
    codigo_inventario = models.CharField(max_length=20, unique=True)
    observacion = models.TextField(blank=True, null=True)
    geom = models.PointField(srid=25830)

    class Meta:
        db_table = "campus_puntos"

    def __str__(self):
        return f"Punto {self.id} - {self.tipo}"


class Linea(models.Model):
    tipo_via = models.CharField(max_length=50)
    pavimento = models.CharField(max_length=50, blank=True, null=True)
    accesible = models.BooleanField(default=True)
    codigo_tramo = models.CharField(max_length=20, unique=True)
    observacion = models.TextField(blank=True, null=True)
    geom = models.LineStringField(srid=25830)
    longitud = models.FloatField(blank=True, null=True, editable=False)

    class Meta:
        db_table = "campus_lineas"

    def save(self, *args, **kwargs):
        # EPSG:25830 esta en metros, por eso geom.length devuelve longitud aproximada en metros.
        if self.geom:
            self.longitud = self.geom.length
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Linea {self.id} - {self.codigo_tramo}"


class Poligono(models.Model):
    nombre = models.CharField(max_length=100)
    uso_principal = models.CharField(max_length=50, blank=True, null=True)
    pisos = models.IntegerField(blank=True, null=True)
    estado = models.CharField(max_length=50, blank=True, null=True)
    observacion = models.TextField(blank=True, null=True)
    geom = models.PolygonField(srid=25830)
    area = models.FloatField(blank=True, null=True, editable=False)
    perimetro = models.FloatField(blank=True, null=True, editable=False)

    class Meta:
        db_table = "campus_poligonos"

    def save(self, *args, **kwargs):
        # EPSG:25830 esta en metros; area en m2 y perimetro en m.
        if self.geom:
            self.area = self.geom.area
            self.perimetro = self.geom.length
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Poligono {self.id} - {self.nombre}"
