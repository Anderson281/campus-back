# scripts/p1/psycampus/puntosOOP.py
# CRUD de campus_puntos usando psycopg y SQL directo.
# Regla espacial: el punto debe estar dentro de algun poligono existente.

from psycopg.rows import dict_row
from myLib.connect import connect
from myLib.p1Settings import EPSG_CODE, SNAP_DISTANCE


class PuntosOOP:
    def __init__(self):
        self.conn = connect()
        self.cur = self.conn.cursor()

    def disconnect(self):
        self.cur.close()
        self.conn.close()

    def _result(self, ok, message, data):
        return {"ok": ok, "message": message, "data": data}

    def _check_keys(self, d, keys):
        for key in keys:
            if key not in d:
                raise Exception(f"Falta el campo: {key}")

    def _is_valid_geom(self, geom_wkt):
        self.cur.execute(
            """
            SELECT ST_IsValid(
                ST_SnapToGrid(ST_GeomFromText(%s, %s), %s)
            )
            """,
            [geom_wkt, EPSG_CODE, SNAP_DISTANCE],
        )
        return self.cur.fetchone()[0]

    def _point_inside_polygon(self, geom_wkt):
        self.cur.execute(
            """
            SELECT id
            FROM campus_poligonos
            WHERE ST_Within(
                ST_SnapToGrid(ST_GeomFromText(%s, %s), %s),
                geom
            )
            LIMIT 1
            """,
            [geom_wkt, EPSG_CODE, SNAP_DISTANCE],
        )
        return len(self.cur.fetchall()) > 0

    def insert(self, d):
        try:
            self._check_keys(
                d,
                ["tipo", "estado", "material", "codigo_inventario", "observacion", "geom"],
            )
            geom = d["geom"]

            if not self._is_valid_geom(geom):
                self.disconnect()
                return self._result(False, "La geometria del punto no es valida", [])

            if not self._point_inside_polygon(geom):
                self.disconnect()
                return self._result(False, "El punto debe estar dentro de un poligono", [])

            self.cur.execute(
                """
                INSERT INTO campus_puntos
                (tipo, estado, material, codigo_inventario, observacion, geom)
                VALUES (%s, %s, %s, %s, %s,
                        ST_SnapToGrid(ST_GeomFromText(%s, %s), %s))
                RETURNING id
                """,
                [
                    d["tipo"],
                    d["estado"],
                    d["material"],
                    d["codigo_inventario"],
                    d["observacion"],
                    geom,
                    EPSG_CODE,
                    SNAP_DISTANCE,
                ],
            )
            row = self.cur.fetchall()
            self.conn.commit()
            self.disconnect()
            return self._result(True, "Inserted", row)
        except Exception as e:
            self.conn.rollback()
            self.disconnect()
            return self._result(False, str(e), [])

    def select(self, d):
        try:
            id_min = int(d.get("id", 0))
            self.cur.execute(
                """
                SELECT id, tipo, estado, material, codigo_inventario, observacion,
                       ST_AsText(geom) AS geom
                FROM campus_puntos
                WHERE id > %s
                ORDER BY id
                """,
                [id_min],
            )
            rows = self.cur.fetchall()
            self.disconnect()
            return self._result(True, "Selected", rows)
        except Exception as e:
            self.disconnect()
            return self._result(False, str(e), [])

    def selectasDict(self, d):
        try:
            id_min = int(d.get("id", 0))
            self.cur.close()
            self.cur = self.conn.cursor(row_factory=dict_row)
            self.cur.execute(
                """
                SELECT id, tipo, estado, material, codigo_inventario, observacion,
                       ST_AsText(geom) AS geom
                FROM campus_puntos
                WHERE id > %s
                ORDER BY id
                """,
                [id_min],
            )
            rows = self.cur.fetchall()
            self.disconnect()
            return self._result(True, "Selected", rows)
        except Exception as e:
            self.disconnect()
            return self._result(False, str(e), [])

    def update(self, d):
        try:
            self._check_keys(
                d,
                ["id", "tipo", "estado", "material", "codigo_inventario", "observacion", "geom"],
            )
            geom = d["geom"]

            if not self._is_valid_geom(geom):
                self.disconnect()
                return self._result(False, "La geometria del punto no es valida", [])

            if not self._point_inside_polygon(geom):
                self.disconnect()
                return self._result(False, "El punto debe estar dentro de un poligono", [])

            self.cur.execute(
                """
                UPDATE campus_puntos
                SET tipo = %s,
                    estado = %s,
                    material = %s,
                    codigo_inventario = %s,
                    observacion = %s,
                    geom = ST_SnapToGrid(ST_GeomFromText(%s, %s), %s)
                WHERE id = %s
                """,
                [
                    d["tipo"],
                    d["estado"],
                    d["material"],
                    d["codigo_inventario"],
                    d["observacion"],
                    geom,
                    EPSG_CODE,
                    SNAP_DISTANCE,
                    int(d["id"]),
                ],
            )
            affected = self.cur.rowcount
            self.conn.commit()
            self.disconnect()
            return self._result(True, "Updated", [{"rows": affected}])
        except Exception as e:
            self.conn.rollback()
            self.disconnect()
            return self._result(False, str(e), [])

    def delete(self, d):
        try:
            self._check_keys(d, ["id"])
            self.cur.execute("DELETE FROM campus_puntos WHERE id = %s", [int(d["id"])])
            affected = self.cur.rowcount
            self.conn.commit()
            self.disconnect()
            return self._result(True, "Deleted", [{"rows": affected}])
        except Exception as e:
            self.conn.rollback()
            self.disconnect()
            return self._result(False, str(e), [])
