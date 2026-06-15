import logica

# --- CONFIGURACIÓN ---
RUTA_CSV = "paises.csv"


# --- FUNCIONES DE MENÚ ---

def mostrar_menu_principal():
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
    print("\n--- FILTRAR POR ---")
    print("1. Continente")
    print("2. Rango de población")
    print("3. Volver")


def mostrar_menu_orden():
    print("\n--- ORDENAR POR ---")
    print("1. Nombre")
    print("2. Población")
    print("3. Superficie")
    print("4. Volver")


# --- FUNCIONES DE PRESENTACIÓN ---

def mostrar_lista(paises):
    # Muestra una lista de países formateada para el usuario
    if not paises:
        print("No hay países para mostrar.")
        return
    print(f"\n{'NOMBRE':<20} {'POBLACIÓN':>15} {'SUPERFICIE (km²)':>17} {'CONTINENTE':<15}")
    print("-" * 70)
    for p in paises:
        print(f"{p['nombre'].capitalize():<20} {p['poblacion']:>15} {p['superficie']:>17} {p['continente'].capitalize():<15}")


# --- FUNCIONES DE INTERACCIÓN ---

def pedir_pais():
    # Pide al usuario los datos de un nuevo país y devuelve el diccionario
    print("\n--- AGREGAR PAÍS ---")
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
    nuevo = pedir_pais()
    exito, mensaje = logica.agregar_pais(nuevo, paises)
    print(mensaje)


def opcion_modificar(paises):
    print("\n--- MODIFICAR PAÍS ---")
    cual      = input("Nombre del país a modificar: ").strip()
    nuevapob  = input("Nueva población: ").strip()
    nuevasup  = input("Nueva superficie (km²): ").strip()
    exito, mensaje = logica.modificar_pais(cual, paises, nuevapob, nuevasup)
    print(mensaje)


def opcion_buscar(paises):
    print("\n--- BUSCAR PAÍS ---")
    cual = input("Ingresá el nombre o parte del nombre: ").strip()
    exito, resultado = logica.buscador(cual, paises)
    print(resultado)


def opcion_filtrar(paises):
    mostrar_menu_filtros()
    opcion = input("Elegí una opción: ").strip()

    if opcion == "1":
        continente = input("Ingresá el continente: ").strip()
        exito, resultado = logica.filtro_cont(paises, continente)
        if exito:
            mostrar_lista(resultado)
        else:
            print(resultado)

    elif opcion == "2":
        pobminima = input("Población mínima: ").strip()
        pobmaxima = input("Población máxima: ").strip()
        # Validamos que sean enteros antes de pasarlos
        if not pobminima.isdigit() or not pobmaxima.isdigit():
            print("Los valores de población deben ser números enteros positivos.")
            return
        exito, resultado = logica.filtro_pob(paises, int(pobminima), int(pobmaxima))
        if exito:
            mostrar_lista(resultado)
        else:
            print(resultado)

    elif opcion == "3":
        return
    else:
        print("Opción inválida.")


def opcion_ordenar(paises):
    mostrar_menu_orden()
    opcion = input("Elegí una opción: ").strip()

    criterios = {"1": "nombre", "2": "poblacion", "3": "superficie"}

    if opcion == "4":
        return
    if opcion not in criterios:
        print("Opción inválida.")
        return

    criterio = criterios[opcion]
    orden = input("¿Orden ascendente o descendente? (asc/desc): ").strip().lower()

    exito, resultado = logica.ordenar_paises(paises, criterio, orden)
    if exito:
        mostrar_lista(resultado)
    else:
        print(resultado)


def opcion_estadisticas(paises):
    exito, mensaje = logica.estadistica(paises)
    print("\n--- ESTADÍSTICAS ---")
    print(mensaje)


# --- PROGRAMA PRINCIPAL ---

def main():
    # Cargamos los datos al inicio del programa
    paises = logica.cargar_csv(RUTA_CSV)
    print(f"Se cargaron {len(paises)} países desde '{RUTA_CSV}'.")

    while True:
        mostrar_menu_principal()
        opcion = input("Elegí una opción: ").strip()

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
            # Guardamos antes de salir
            exito = logica.guardar_csv(RUTA_CSV, paises)
            if exito:
                print("Datos guardados correctamente. ¡Hasta luego!")
            else:
                print("No había datos para guardar. ¡Hasta luego!")
            break
        else:
            print("Opción inválida. Ingresá un número del 1 al 7.")


main()
