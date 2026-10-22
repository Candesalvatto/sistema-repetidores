DROP VIEW IF EXISTS vista_matricula_completa;

CREATE VIEW vista_matricula_completa AS
SELECT 
    m.id_matricula,
    d.n_departamento,
    c.ciclo_lectivo,
    n.n_nivel,
    m.n_anio_grado,
    m.estudiantes,
    m.repetidores,
    m.sobreedad,
    ROUND((CAST(m.repetidores AS DECIMAL(10,2)) / NULLIF(m.estudiantes, 0)) * 100, 2) AS tasa_repitencia,
    ROUND((CAST(m.sobreedad AS DECIMAL(10,2)) / NULLIF(m.estudiantes, 0)) * 100, 2) AS tasa_sobreedad
FROM matricula m
INNER JOIN departamentos d ON m.id_departamento = d.id_departamento
INNER JOIN ciclo_lectivo c ON m.id_ciclo = c.id_ciclo
INNER JOIN nivel_educativo n ON m.id_nivel = n.id_nivel;