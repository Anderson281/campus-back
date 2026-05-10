# scripts/p1/psycampus/poligonosOOP.py
# CRUD de campus_poligonos usando psycopg y SQL directo.
# Regla espacial: un poligono no debe cruzarse/intersecarse realmente con otro poligono.

from psycopg.rows import dict_row
from myLib.connect import connect
from myLib.p1Settings import EPSG_CODE, SNAP_DISTANCE


class PoligonosOOP:
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

    def _has_real_intersection(self, geom_wkt, exclude_id=None):
        params = [geom_wkt, EPSG_CODE, SNAP_DISTANCE]
        extra = ""
        if exclude_id is not None:
            extra = "AND id != %s"
            params.append(int(exclude_id))

        self.cur.execute(
            f"""
            SELECT id
            FROM campus_poligonos
            WHERE ST_Relate(
                geom,
                ST_SnapToGrid(ST_GeomFromText(%s, %s), %s),
                'T********'
            )
            {extra}
            """,
            params,
        )
        return self.cur.fetchall()

    def insert(self, d):
        try:
            self._check_keys(
                d,
                ["nombre", "uso_principal", "pisos", "estado", "observacion", "geom"],
            )
            geom = d["geom"]

            if not self._is_valid_geom(geom):
                self.disconnect()
                return self._result(False, "La geometria del poligono no es valida", [])

            rows = self._has_real_intersection(geom)
            if len(rows) > 0:
                self.disconnect()
                return self._result(False, "El poligono se interseca con otro poligono", rows)

            self.cur.execute(
                """
                INSERT INTO campus_poligonos
                (nombre, uso_principal, pisos, estado, observacion, geom)
                VALUES (%s, %s, %s, %s, %s,
                        ST_SnapToGrid(ST_GeomFromText(%s, %s), %s))
                RETURNING id
                """,
                [
                    d["nombre"],
                    d["uso_principal"],
                    int(d["pisos"]) if d["pisos"] not in [None, ""] else None,
                    d["estado"],
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
                SELECT id, nombre, uso_principal, pisos, estado, observacion,
                       area, perimetro, ST_AsText(geom) AS geom
                FROM campus_poligonos
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
                SELECT id, nombre, uso_principal, pisos, estado, observacion,
                       area, perimetro, ST_AsText(geom) AS geom
                FROM campus_poligonos
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
                ["id", "nombre", "uso_principal", "pisos", "estado", "observacion", "geom"],
            )
            geom = d["geom"]

            if not self._is_valid_geom(geom):
                self.disconnect()
                return self._result(False, "La geometria del poligono no es valida", [])

            rows = self._has_real_intersection(geom, exclude_id=d["id"])
            if len(rows) > 0:
                self.disconnect()
                return self._result(False, "El poligono se interseca con otro poligono", rows)

            self.cur.execute(
                """
                UPDATE campus_poligonos
                SET nombre = %s,
                    uso_principal = %s,
                    pisos = %s,
                    estado = %s,
                    observacion = %s,
                    geom = ST_SnapToGrid(ST_GeomFromText(%s, %s), %s)
                WHERE id = %s
                """,
                [
                    d["nombre"],
                    d["uso_principal"],
                    int(d["pisos"]) if d["pisos"] not in [None, ""] else None,
                    d["estado"],
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
            self.cur.execute("DELETE FROM campus_poligonos WHERE id = %s", [int(d["id"])])
            affected = self.cur.rowcount
            self.conn.commit()
            self.disconnect()
            return self._result(True, "Deleted", [{"rows": affected}])
        except Exception as e:
            self.conn.rollback()
            self.disconnect()
            return self._result(False, str(e), [])
