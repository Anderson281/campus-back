DROP TABLE IF EXISTS campus_puntos CASCADE;
CREATE TABLE campus_puntos (
    id SERIAL PRIMARY KEY,
    tipo VARCHAR(50) NOT NULL,
    estado VARCHAR(50) NOT NULL,
    material VARCHAR(50),
    codigo_inventario VARCHAR(20) UNIQUE,
    observacion TEXT,
    geom geometry(Point, 25830) NOT NULL
);
CREATE INDEX campus_puntos_gix ON campus_puntos USING GIST (geom);
DROP TABLE IF EXISTS campus_lineas CASCADE;
CREATE TABLE campus_lineas (
    id SERIAL PRIMARY KEY,
    tipo_via VARCHAR(50) NOT NULL,
    pavimento VARCHAR(50),
    accesible BOOLEAN DEFAULT TRUE,
    codigo_tramo VARCHAR(20) UNIQUE,
    observacion TEXT,
    geom geometry(LineString, 25830) NOT NULL,
    longitud DOUBLE PRECISION GENERATED ALWAYS AS (ST_Length(geom)) STORED
);
CREATE INDEX campus_lineas_gix ON campus_lineas USING GIST (geom);
DROP TABLE IF EXISTS campus_poligonos CASCADE;
CREATE TABLE campus_poligonos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    uso_principal VARCHAR(50),
    pisos INTEGER,
    estado VARCHAR(50),
    observacion TEXT,
    geom geometry(Polygon, 25830) NOT NULL,
    area DOUBLE PRECISION GENERATED ALWAYS AS (ST_Area(geom)) STORED,
    perimetro DOUBLE PRECISION GENERATED ALWAYS AS (ST_Perimeter(geom)) STORED
);
CREATE INDEX campus_poligonos_gix ON campus_poligonos USING GIST (geom)