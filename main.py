import logica

# --- CONFIGURACIÓN ---
RUTA_CSV = "data.csv"


# --- FUNCIONES DE MENÚ ---

def mostrar_menu_principal():
    """
    Imprime en consola las opciones del sistema de gestión principal.
    """
    print("\n========== GESTIÓN DE PAÍSES ==========")
    print("1. Agregar un país")
    print("2. Modificar población y superficie de un país")
    print("3. Buscar un país por nombre")
    print("4. Filtrar países")
    print("5. Ordenar países")
    print("6. Ver estadísticas")
    print("7. Guardar y salir")
    print("========================================")


def mostrar_menu_filtros():
    """
    CORRECCIÓN / REQUERIMIENTO: Se añade la opción 3 para cumplir 
    con el filtrado por rango de superficie exigido en la consigna.
    """
    print("\n--- FILTRAR POR ---")
    print("1. Continente")
    print("2. Rango de población")
    print("3. Rango de superficie (km²)") # Opción sumada
    print("4. Volver")                     # Desplazado a opción 4


def mostrar_menu_orden():
    """
    Imprime las propiedades disponibles por las cuales ordenar el dataset.
    """
    print("\n--- ORDENAR POR ---")
    print("1. Nombre")
    print("2. Población")
    print("3. Superficie")
    print("4. Volver")


# --- FUNCIONES DE PRESENTACIÓN ---

def mostrar_lista(paises):
    """
    Muestra una lista de países formateada en columnas tabuladas de forma estética.
    """
    if not paises:
        print("No hay países para mostrar.")
        return # Si no hay datos en la lista, cortamos la ejecución de la función temprano
        
    # Imprimimos la cabecera usando alineaciones: '<' izquierda, '>' derecha con anchos fijos
    print(f"\n{'NOMBRE':<20} {'POBLACIÓN':>15} {'SUPERFICIE (km²)':>17} {'CONTINENTE':<15}")
    print("-" * 70) # Línea divisoria estricta de 70 caracteres para prolijidad visual
    for p in paises:
        # Iteramos cada país aplicando .capitalize() para homogeneizar la visualización final en consola
        print(f"{p['nombre'].capitalize():<20} {p['poblacion']:>15} {p['superficie']:>17} {p['continente'].capitalize():<15}")


# --- FUNCIONES DE INTERACCIÓN ---

def pedir_pais():
    """
    Solicita por teclado las propiedades de un país y retorna un diccionario intermedio.
    """
    print("\n--- AGREGAR PAÍS ---")
    # Capturamos los datos quitando espacios en blanco accidentales en los extremos con .strip()
    nombre     = input("Nombre del país: ").strip()
    poblacion  = input("Población: ").strip()
    superficie = input("Superficie (km²): ").strip()
    continente = input("Continente: ").strip()
    return {
        "nombre": nombre,
        "poblacion": poblacion,
        "superficie": superficie,
        "continente": continente
    }


def opcion_agregar(paises):
    """
    Se comunica con la capa de lógica para validar e intentar dar de alta un país en memoria.
    """
    nuevo = pedir_pais() # Invocamos la función interactiva para obtener los datos crudos del usuario
    exito, mensaje = logica.agregar_pais(nuevo, paises) # Desempaquetamos la tupla de retorno (bool, str)
    print(mensaje) # Mostramos el mensaje claro de éxito o la razón exacta del rechazo de la validación


def opcion_modificar(paises):
    """
    Solicita las claves necesarias para alterar la población y superficie de un registro existente.
    """
    print("\n--- MODIFICAR PAÍS ---")
    cual      = input("Nombre del país a modificar: ").strip()
    nuevapob  = input("Nueva población: ").strip()
    nuevasup  = input("Nueva superficie (km²): ").strip()
    # Enviamos los datos crudos a la lógica; esta se encargará de validar tipos y positividad
    exito, mensaje = logica.modificar_pais(cual, paises, nuevapob, nuevasup)
    print(mensaje)


def opcion_buscar(paises):
    """
    Pide un patrón de caracteres para buscar países por coincidencia parcial.
    """
    print("\n--- BUSCAR PAÍS ---")
    cual = input("Ingresá el nombre o parte del nombre: ").strip()
    exito, resultado = logica.buscador(cual, paises)
    print(resultado) # Imprime el listado ordenado de coincidencias o el mensaje de error provisto


def opcion_filtrar(paises):
    """
    Controlador para bifurcar el filtrado del dataset según la propiedad elegida.
    """
    mostrar_menu_filtros()
    opcion = input("Elegí una opción: ").strip()

    if opcion == "1":
        continente = input("Ingresá el continente: ").strip()
        exito, resultado = logica.filtro_cont(paises, continente)
        if exito:
            mostrar_lista(resultado) # Si el filtro arrojó países, los mostramos tabulados
        else:
            print(resultado)         # Caso contrario, 'resultado' contiene el string de error

    elif opcion == "2":
        pobminima = input("Población mínima: ").strip()
        pobmaxima = input("Población máxima: ").strip()
        # Validación defensiva: Verificamos con .isdigit() que las entradas contengan únicamente dígitos numéricos
        if not pobminima.isdigit() or not pobmaxima.isdigit():
            print("Los valores de población deben ser números enteros positivos.")
            return # Interrumpimos la ejecución de la función para evitar crasheos por ValueError
        exito, resultado = logica.filtro_pob(paises, int(pobminima), int(pobmaxima))
        if exito:
            mostrar_lista(resultado)
        else:
            print(resultado)

    elif opcion == "3":
        # REQUERIMIENTO COMPLEMENTADO: Captura de datos para el filtro por rango de superficie
        supminima = input("Superficie mínima (km²): ").strip()
        supmaxima = input("Superficie máxima (km²): ").strip()
        # Validación defensiva en la interfaz para certificar que sean enteros antes de procesar
        if not supminima.isdigit() or not supmaxima.isdigit():
            print("Los valores de superficie deben ser números enteros positivos.")
            return
        exito, resultado = logica.filtro_sup(paises, int(supminima), int(supmaxima))
        if exito:
            mostrar_lista(resultado)
        else:
            print(resultado)

    elif opcion == "4":
        return # Retorno vacío para regresar limpiamente al bucle principal sin realizar acciones
    else:
        print("Opción inválida.")


def opcion_ordenar(paises):
    """
    Maneja los parámetros requeridos por el algoritmo de ordenamiento incorporado.
    """
    mostrar_menu_orden()
    opcion = input("Elegí una opción: ").strip()

    # Mapeamos la selección del menú con las llaves que manejan internamente nuestros diccionarios
    criterios = {"1": "nombre", "2": "poblacion", "3": "superficie"}

    if opcion == "4":
        return
    if opcion not in criterios:
        print("Opción inválida.")
        return

    criterio = criterios[opcion] # Extraemos el string del criterio ('nombre', 'poblacion' o 'superficie')
    orden = input("¿Orden ascendente o descendente? (asc/desc): ").strip().lower()

    exito, resultado = logica.ordenar_paises(paises, criterio, orden)
    if exito:
        mostrar_lista(resultado) # Imprime la lista ordenada de forma reluciente en consola
    else:
        print(resultado)


def opcion_estadisticas(paises):
    """
    Muestra en pantalla el bloque resumido de cálculos métricos del dataset.
    """
    exito, mensaje = logica.estadistica(paises)
    print("\n--- ESTADÍSTICAS ---")
    print(mensaje)


# --- PROGRAMA PRINCIPAL ---

def main():
    """
    Punto de entrada principal del programa. Coordina el ciclo de vida de la aplicación.
    """
    # Flujo de arranque: Cargamos en memoria la lista de países leyendo el archivo CSV especificado
    paises = logica.cargar_csv(RUTA_CSV)
    print(f"Se cargaron {len(paises)} países desde '{RUTA_CSV}'.")

    # Bucle infinito controlado para sostener el menú de consola interactivo en ejecución continuo
    while True:
        mostrar_menu_principal()
        opcion = input("Elegí una opción: ").strip()

        # Estructura condicional anidada para despachar las funciones de interacción según la opción
        if opcion == "1":
            opcion_agregar(paises)
        elif opcion == "2":
            opcion_modificar(paises)
        elif opcion == "3":
            opcion_buscar(paises)
        elif opcion == "4":
            opcion_filtrar(paises)
        elif opcion == "5":
            opcion_ordenar(paises)
        elif opcion == "6":
            opcion_estadisticas(paises)
        elif opcion == "7":
            # Persistencia de datos obligatoria: Guardamos todo el estado de la memoria en el archivo CSV
            exito = logica.guardar_csv(RUTA_CSV, paises)
            if exito:
                print("Datos guardados correctamente en el archivo. ¡Hasta luego!")
            else:
                print("No había datos para guardar o hubo un error en la escritura. ¡Hasta luego!")
            break # Rompe el bucle 'while True', permitiendo finalizar el script de manera ordenada
        else:
            print("Opción inválida. Ingresá un número del 1 al 7.")

# Ejecución condicional estándar: Garantiza que el programa corra inmediatamente al ser invocado de forma directa
if __name__ == "__main__":
    main()
