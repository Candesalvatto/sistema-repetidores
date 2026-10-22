# NotFound: Sistema de gestión y análisis de repitencia y sobreedad (Córdoba, 2021-2025)

Proyecto integrador ABP del módulo Innovación en Gestión de Datos
(Programación I y Bases de Datos II), Tecnicatura Superior en Ciencia de Datos e
Inteligencia Artificial, ISPC. Grupo 10 "NotFound", Comisión B2, Cohorte 2026.

Integrantes: Candela Salvatto, Martin Regis, Bruno Oliva, Ontivero Ailin,
Torres Eric, Van Norden Jordi Emiliano, Joaquin Soria.

## Qué hace

Guarda en MySQL los datos de estudiantes, repetidores y sobreedad de la provincia
de Córdoba (26 departamentos, 2021-2025, 1.690 registros), permite gestionarlos desde
un menú por consola (alta, baja, modificación y búsquedas) y los analiza con
Pandas y NumPy para responder: ¿en qué grados del secundario se concentra la
repitencia y en qué departamentos conviene focalizar el refuerzo?

## Requisitos

- Python 3.11 o superior
- MySQL Server 8.0 (con el plugin `mysql_native_password` habilitado) y MySQL Workbench

## Instalación

1. Descomprimir la carpeta del proyecto y abrir una terminal dentro de ella.
2. Crear y activar un entorno virtual:
   - Windows: `python -m venv .venv` y luego `.venv\Scripts\activate`
   - Linux o Mac: `python3 -m venv .venv` y luego `source .venv/bin/activate`
3. Instalar las librerías: `pip install -r requirements.txt`
4. Crear la base de datos: abrir `ABP_BD_NotFound.sql` en MySQL Workbench y
   ejecutarlo completo (ícono del rayo). El script crea la base `repetidores`, las
   tablas, la vista `vista_matricula_completa` y carga los 1.690 registros.
5. Configurar la conexión: copiar `.env.ejemplo` con el nombre `.env` y completar
   los datos de tu MySQL. Las variables son:
   - `DB_HOST`: servidor (por defecto `localhost`)
   - `DB_USER`: usuario (por defecto `root`)
   - `DB_PASSWORD`: contraseña (obligatoria)
   - `DB_NAME`: nombre de la base (por defecto `repetidores`)
   - `DB_PORT`: puerto (por defecto `3306`)

   El archivo `.env` real no se entrega, porque contiene la contraseña.

## Ejecución

- Menú de la aplicación: `python main.py`
- Análisis de datos (Pandas y NumPy): `python procesamiento.py`

## Estructura

- `main.py`: punto de entrada, abre el menú.
- `config/database.py`: conexión a MySQL (lee los datos del `.env`).
- `models/`: una clase por tabla (Departamento, CicloLectivo, NivelEducativo, Matricula).
- `views/menu.py`: menú por consola con 7 opciones.
- `scripts/create_views.sql`: definición de la vista.
- `procesamiento.py`: módulo de análisis con Pandas y NumPy.
- `ABP_BD_NotFound.sql`: script único de la base de datos.
- `requirements.txt` y `.env.ejemplo`.

## Repositorio

[Pegar acá el enlace, si lo tienen. Si no, borrar esta sección.]