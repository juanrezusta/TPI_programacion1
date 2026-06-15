# Gestión de Datos de Países en Python

**Trabajo Práctico Integrador — Programación 1**  
Tecnicatura Universitaria en Programación — UTN TUPD  
Cohorte Marzo 2026

---

## Integrantes

| Nombre | Comisión |
|--------|----------|
| Juan Manuel Garcia Rezusta | Comisión 22 |
| Tomas Rebottaro | Comisión 4 |

---

## Descripción

Aplicación de consola desarrollada en Python que permite gestionar un dataset de países. Lee y escribe datos desde un archivo CSV, y ofrece un menú interactivo para agregar registros, modificarlos, buscarlos, filtrarlos, ordenarlos y ver estadísticas generales.

El proyecto está dividido en dos módulos con responsabilidades claramente separadas:

| Archivo | Responsabilidad |
|---------|----------------|
| `logica.py` | Toda la lógica de negocio: validaciones, operaciones sobre datos, filtros, estadísticas y acceso al CSV |
| `main.py` | Menú interactivo, entrada del usuario y presentación de resultados en consola |
| `data.csv` | Dataset base con los registros de países |

---

## Requisitos

- Python 3.x
- Sin dependencias externas — solo usa el módulo `csv` de la biblioteca estándar

---

## Instalación y uso

1. Clonar o descargar el repositorio
2. Verificar que `logica.py`, `main.py` y `data.csv` estén en la misma carpeta
3. Ejecutar desde la terminal:

```bash
python main.py
```

4. Navegar el menú con los números del 1 al 7
5. Al elegir la opción **7 (Guardar y salir)**, los cambios se persisten en `data.csv`

---

## Estructura del proyecto

```
├── main.py         # Menú e interacción con el usuario
├── logica.py       # Lógica de negocio y funciones principales
├── data.csv        # Dataset base con países de ejemplo
└── README.md       # Este archivo
```

---

## Funcionalidades

| Opción | Descripción |
|--------|-------------|
| 1 | Agregar un nuevo país (nombre, población, superficie, continente) |
| 2 | Modificar población y superficie de un país existente |
| 3 | Buscar un país por nombre (coincidencia parcial) |
| 4 | Filtrar por continente, rango de población o rango de superficie |
| 5 | Ordenar por nombre, población o superficie (ascendente o descendente) |
| 6 | Ver estadísticas generales del dataset |
| 7 | Guardar cambios en `data.csv` y salir |

---

## Ejemplos de entrada/salida

### Agregar un país
```
Nombre del país: Uruguay
Población: 3473730
Superficie (km²): 176215
Continente: América

País agregado correctamente.
```

### Buscar por nombre
```
Ingresá el nombre o parte del nombre: ar

Tu palabra ingresada 'ar' tiene 2 coincidencia/s:
Argentina | población: 45376763 | superficie: 2780400 km² | continente: América.
Brasil | población: 213993437 | superficie: 8515767 km² | continente: América.
```

### Filtrar por rango de población
```
Población mínima: 50000000
Población máxima: 150000000

NOMBRE                      POBLACIÓN   SUPERFICIE (km²) CONTINENTE
----------------------------------------------------------------------
Francia                      67391582            551695  Europa
Italia                       60367477            301340  Europa
...
```

### Ordenar por superficie descendente
```
¿Orden ascendente o descendente? (asc/desc): desc

NOMBRE                      POBLACIÓN   SUPERFICIE (km²) CONTINENTE
----------------------------------------------------------------------
China                      1444216107          9596960  Asia
Australia                    25499884          7692024  Oceanía
...
```

### Estadísticas
```
El país más poblado es China, con 1444216107 habitantes.
El país menos poblado es Nueva Zelanda, con 5084300 habitantes.
El promedio total de la población según los países cargados es de: 200129524 habitantes por país.
El promedio de la superficie de entre todos los países cargados es de: 2407756 km².

Cantidad de países por continente:
 - América: 5 país/es
 - Europa: 5 país/es
 - Asia: 5 país/es
 - África: 5 país/es
 - Oceanía: 2 país/es
```

---

## Formato del CSV

El archivo `data.csv` debe respetar el siguiente formato:

```
nombre,poblacion,superficie,continente
Argentina,45376763,2780400,América
Japón,125800000,377975,Asia
```

| Campo | Tipo | Restricción |
|-------|------|-------------|
| `nombre` | string | No puede estar vacío |
| `poblacion` | entero | Debe ser positivo |
| `superficie` | entero | Debe ser positivo (en km²) |
| `continente` | string | No puede estar vacío |

---

## Patrón de diseño

Todas las funciones de `logica.py` retornan una tupla `(booleano, resultado)`:

- Si el booleano es `True`, el resultado es el dato o mensaje de éxito
- Si el booleano es `False`, el resultado es el mensaje de error

Esto permite que `main.py` maneje cualquier caso de forma uniforme y consistente.

---

## Participación de los integrantes

El diseño general del proyecto — la arquitectura en dos módulos, la decisión de usar una lista de diccionarios como estructura central y el patrón de retorno `(booleano, mensaje)` para todas las funciones — fue discutido y definido en conjunto.

| Integrante | Contribución |
|------------|-------------|
| Juan Manuel Garcia Rezusta | Desarrollo completo de `logica.py`: validaciones, altas, modificaciones, búsqueda, filtros, ordenamientos, estadísticas y manejo del CSV. Armado de estructura. |
| Tomas Rebottaro | Desarrollo completo de `main.py`: menú interactivo, submenús, funciones de presentación y conexión con `logica.py`. QA del sistema completo: pruebas de flujos, casos borde y validación de mensajes al usuario. |

---

## Links

- 🎥 Video demostrativo: FALTA AGREGARRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR
