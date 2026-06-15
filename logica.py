import csv

def cargar_csv(ruta):
    """
    Lee los datos desde un archivo CSV y devuelve una lista de diccionarios.
    Maneja de manera robusta los errores de formato y filas mal formadas.
    """
    paises = [] # Inicializamos una lista vacía donde acumularemos los diccionarios de cada país
    try:
        # Abrimos el archivo en modo lectura ('r') con codificación UTF-8 para soportar tildes
        with open(ruta, newline='', encoding='utf-8') as archivo:
            # Creamos un lector de diccionarios; mapea automáticamente la primera fila como llaves
            lector = csv.DictReader(archivo)
            
            # Control de errores: Validamos que el archivo contenga cabeceras válidas en su primera línea
            if lector.fieldnames is None:
                print("Error: El archivo CSV no posee una fila de encabezados.")
                return paises

            # Iteramos fila por fila. Usamos 'enumerate' empezando en 2 para rastrear el número real de fila en el archivo
            for nro_fila, fila in enumerate(lector, start=2):
                try:
                    # VALIDACIÓN: Verificamos si alguna de las celdas obligatorias llegó vacía o inexistente
                    if not fila.get("nombre") or not fila.get("poblacion") or not fila.get("superficie") or not fila.get("continente"):
                        print(f"⚠️ Fila {nro_fila} omitida: contiene campos obligatorios vacíos.")
                        continue # Si falta un dato, salteamos esta fila con 'continue' y pasamos a la siguiente
                    
                    # Estructuramos el diccionario del país normalizando los textos y convirtiendo los números
                    pais = {
                        "nombre": fila["nombre"].strip().lower(),      # Eliminamos espacios extras y pasamos a minúsculas
                        "poblacion": int(fila["poblacion"]),           # Convertimos a entero (puede lanzar ValueError si hay letras)
                        "superficie": int(fila["superficie"]),         # Convertimos a entero (puede lanzar ValueError si hay letras)
                        "continente": fila["continente"].strip().lower() # Limpiamos espacios y estandarizamos a minúsculas
                    }
                    paises.append(pais) # Si la conversión fue exitosa, añadimos el diccionario a nuestra lista
                except (ValueError, TypeError, KeyError):
                    # Captura fallos si se intentó pasar texto a int o si una columna clave no existe en la fila
                    print(f"⚠️ Fila {nro_fila} omitida: error de formato en datos numéricos.")
                    continue # Ignoramos la fila corrupta y continuamos con el procesamiento del archivo
    except FileNotFoundError:
        # En caso de que el archivo no exista en el directorio, evitamos que el programa explote catastróficamente
        print(f"Advertencia: Archivo '{ruta}' no encontrado. Se iniciará una lista vacía.")
    return paises # Retornamos la lista final (ya sea con datos cargados o vacía)


def guardar_csv(ruta, paises):
    """
    Guarda la lista de países en un archivo CSV, formateando los textos
    con capitalización estética antes de la escritura.
    """
    if not paises:
        return False # Si la lista está vacía, no hay nada que escribir; retornamos falso
    
    # Definimos el orden exacto de las columnas que tendrá nuestro archivo CSV de salida
    encabezados = ["nombre", "poblacion", "superficie", "continente"]
    try:
        # Abrimos el archivo en modo escritura ('w'), pisando lo anterior de forma segura
        with open(ruta, "w", newline='', encoding='utf-8') as archivo:
            # Configuramos el escritor dictaminando los encabezados correspondientes
            paquete = csv.DictWriter(archivo, fieldnames=encabezados)
            paquete.writeheader() # Escribimos la primera fila con los nombres de las columnas
            
            paises_formateados = [] # Lista temporal para no alterar los datos en minúsculas del programa en ejecución
            for p in paises:
                # Capitalizamos estéticamente la primera letra de los nombres y continentes para el archivo final
                p_formato = {
                    "nombre": p["nombre"].capitalize(),
                    "poblacion": p["poblacion"],
                    "superficie": p["superficie"],
                    "continente": p["continente"].capitalize()
                }
                paises_formateados.append(p_formato)
            
            paquete.writerows(paises_formateados) # Escribimos todas las filas formateadas juntas
            return True # Operación exitosa
    except Exception:
        return False # Retornamos falso si hubo algún problema con los permisos del archivo o el disco


def validar_estructura(nuevo):
    """
    Valida que el objeto sea un diccionario y contenga todas las llaves requeridas.
    """
    # Verificamos que la variable sea efectivamente de tipo diccionario
    if not isinstance(nuevo, dict):
        return (False, "El dato a ingresar no es del formato adecuado.")
    
    # Recorremos las llaves obligatorias para comprobar que ninguna falda o sea nula
    for llave in ["nombre", "poblacion", "superficie", "continente"]:
        if llave not in nuevo or nuevo[llave] is None:
            return (False, f"El dato a ingresar no está completo. Falta el campo '{llave}'.")
    return (True, "Validación exitosa")


def validar_datos(nuevo):
    """
    Verifica que los tipos de datos internos y sus restricciones numéricas sean válidos.
    """
    # Comprobamos que el nombre sea una cadena de texto no vacía
    if not isinstance(nuevo["nombre"], str) or nuevo["nombre"].strip() == "":
        return (False, "Nombre inválido.")

    try:
        # Evaluamos que la población sea mayor a cero tras asegurar su conversión a entero
        if int(nuevo["poblacion"]) <= 0:
            return (False, "Población inválida. Debe ser un número entero positivo.")
    except (ValueError, TypeError):
        return (False, "Población inválida. Debe ser un número entero positivo.")

    try:
        # Evaluamos que la superficie sea mayor a cero tras asegurar su conversión a entero
        if int(nuevo["superficie"]) <= 0:
            return (False, "Superficie inválida. Debe ser un número entero positivo.")
    except (ValueError, TypeError):
        return (False, "Superficie inválida. Debe ser un número entero positivo.")

    # Comprobamos que el continente sea una cadena de texto no vacía
    if not isinstance(nuevo["continente"], str) or nuevo["continente"].strip() == "":
        return (False, "Continente inválido.")
    
    return (True, "Validación exitosa")


def ya_existe_pais(nombre_pais, paises):
    """
    Comprueba si un país ya se encuentra registrado (búsqueda exacta insensible a mayúsculas).
    """
    nombre_buscado = str(nombre_pais).strip().lower() # Estandarizamos la entrada para comparar limpiamente
    for item in paises:
        # Si coincide el nombre transformado, significa que el país ya está duplicado en la lista
        if nombre_buscado == item["nombre"]:
            return True # Corta la ejecución y confirma la existencia
    return False # Si recorrió todo el bucle y no encontró coincidencia, el país es nuevo


def agregar_pais(nuevo, paises):
    """
    Efectúa el flujo completo de validaciones para agregar un nuevo país a la lista.
    """
    # 1. Validamos que el diccionario tenga todos los campos requeridos
    valido, mensaje = validar_estructura(nuevo)
    if not valido:
        return (False, mensaje)
    
    # 2. Validamos que el contenido de los campos cumpla los tipos y rangos lógicos
    valido, mensaje = validar_datos(nuevo)
    if not valido:
        return (False, mensaje)
    
    # 3. Validamos que el país no se encuentre repetido en nuestra base de datos
    if ya_existe_pais(nuevo["nombre"], paises):
        return (False, "El país que quiere agregar ya se encuentra en la base de datos.")

    # Construimos el registro limpio y normalizado para mantener la consistencia de los datos
    linea_nueva = {
        "nombre": nuevo["nombre"].strip().lower(), 
        "poblacion": int(nuevo["poblacion"]),
        "superficie": int(nuevo["superficie"]),
        "continente": nuevo["continente"].strip().lower()
    }
    paises.append(linea_nueva) # Agregamos el nuevo diccionario a la lista en memoria
    return (True, "País agregado correctamente.")


def modificar_pais(cual, paises, nuevapob, nuevasup):
    """
    Busca un país específico y actualiza sus valores de población y superficie.
    """
    # Validamos primeramente que el país a modificar efectivamente exista
    if not ya_existe_pais(cual, paises):
        return (False, "El país ingresado para modificar no se encuentra registrado previamente.")

    try:
        # Forzamos la conversión a enteros para garantizar la sanidad de los nuevos datos numéricos
        nuevapob = int(nuevapob)
        nuevasup = int(nuevasup)
    except (ValueError, TypeError):
        return (False, "Los datos ingresados para población o superficie no son del tipo adecuado.")

    # Los valores demográficos y geográficos obligatoriamente deben ser mayores a cero
    if nuevapob <= 0 or nuevasup <= 0:
        return (False, "Los datos ingresados para población o superficie deben ser positivos.")
    
    cual_buscado = cual.strip().lower() # Estandarizamos el parámetro de búsqueda

    # Buscamos la coincidencia exacta para aplicar la modificación directa sobre el diccionario
    for item in paises:
        if cual_buscado == item["nombre"]:
            item["poblacion"] = nuevapob   # Reemplazamos la población vieja por la nueva
            item["superficie"] = nuevasup # Reemplazamos la superficie vieja por la nueva
            break # Optimizamos el bucle: una vez encontrado y modificado, salimos del ciclo

    return (True, "El país fue modificado correctamente.")


def buscador(cual, paises):
    """
    Realiza una búsqueda por coincidencia parcial y devuelve una cadena formateada con los resultados.
    """
    coinciden = [] # Lista donde guardaremos los países que hagan match
    cual = cual.lower().strip() # Limpiamos y pasamos a minúsculas el término de búsqueda
    if not cual:
        return (False, "Ingrese un nombre de país válido.")

    # Recorremos la lista evaluando subcadenas
    for item in paises:
        # El operador 'in' chequea si el término ingresado está contenido dentro del nombre del país
        if cual in item["nombre"]:
            coinciden.append(item) # Si contiene la subcadena, lo sumamos a los resultados

    if not coinciden:
        return (False, "El país ingresado no se encuentra en la base de datos.")

    # Construimos el reporte de salida uniendo strings de forma prolija
    lista_mensajes = [f"Tu palabra ingresada '{cual}' tiene {len(coinciden)} de coincidencia/s:"]
    for item in coinciden:
        # Formateamos cada país usando .capitalize() para que la salida en consola sea elegante
        mensaje = f"{item['nombre'].capitalize()} | población: {item['poblacion']} | superficie: {item['superficie']} km² | continente: {item['continente'].capitalize()}."
        lista_mensajes.append(mensaje)

    resultado = "\n".join(lista_mensajes) # Unimos todas las líneas usando saltos de línea
    return (True, resultado)


def estadistica(paises):
    """
    Calcula y construye un reporte de texto con indicadores estadísticos clave.
    """
    if not paises:
        return (False, "No hay datos cargados.")

    # Tomamos el primer país como referencia inicial para los algoritmos de máximo y mínimo
    primero = paises[0]
    mas_poblado = primero
    menos_poblado = primero
    pob_promedio = 0    # Acumulador para la población total
    sup_promedio = 0    # Acumulador para la superficie total
    conteo_continentes = {} # Diccionario para realizar frecuencias (conteo por categorías)

    for item in paises:
        pob_promedio += item["poblacion"]   # Sumamos la población al acumulador global
        sup_promedio += item["superficie"] # Sumamos la superficie al acumulador global

        # Algoritmo de Máximo: Si encontramos una población mayor, actualizamos nuestra referencia
        if item["poblacion"] > mas_poblado["poblacion"]:
            mas_poblado = item

        # Algoritmo de Mínimo: Si encontramos una población menor, actualizamos nuestra referencia
        if item["poblacion"] < menos_poblado["poblacion"]:
            menos_poblado = item
            
        # Lógica de conteo de categorías (Continentes)
        cont = item["continente"].capitalize()
        if cont in conteo_continentes:
            conteo_continentes[cont] += 1 # Si el continente ya existía en el diccionario, sumamos 1
        else:
            conteo_continentes[cont] = 1  # Si aparece por primera vez, lo inicializamos en 1

    # Calculamos las medias aritméticas dividiendo los totales acumulados por la cantidad de países
    pob_promedio = pob_promedio / len(paises)
    sup_promedio = sup_promedio / len(paises)

    # Armamos las líneas correspondientes al desglose por continente
    lineas_continentes = []
    for cont, cant in conteo_continentes.items():
        lineas_continentes.append(f" - {cont}: {cant} país/es")
    texto_continentes = "\n".join(lineas_continentes)

    # Construimos el texto final usando f-strings y formateando con 'round' para evitar decimales molestos
    mensaje = f'''El país más poblado es {mas_poblado["nombre"].capitalize()}, con {mas_poblado["poblacion"]} habitantes.
El país menos poblado es {menos_poblado["nombre"].capitalize()}, con {menos_poblado["poblacion"]} habitantes.
El promedio total de la población según los países cargados es de: {round(pob_promedio)} habitantes por país.
El promedio de la superficie de entre todos los países cargados es de: {round(sup_promedio)} km².

Cantidad de países por continente:
{texto_continentes}'''
    
    return (True, mensaje)


# Funciones auxiliares requeridas por la función built-in 'sorted' para extraer las llaves de ordenamiento
def saca_nombre(p): 
    return p["nombre"]

def saca_poblacion(p): 
    return p["poblacion"]

def saca_superficie(p): 
    return p["superficie"]


def ordenar_paises(paises, criterio, orden):
    """
    Ordena los países según el criterio indicado ('nombre', 'poblacion', 'superficie') 
    y el sentido de ordenamiento ('asc' o 'desc').
    """
    if not paises:
        return (False, "No hay datos cargados.")

    # Bifurcamos según el criterio pasando la función extractora correspondiente al parámetro 'key'
    if criterio == "nombre":
        lista = sorted(paises, key=saca_nombre)
    elif criterio == "poblacion":
        lista = sorted(paises, key=saca_poblacion)
    elif criterio == "superficie":
        lista = sorted(paises, key=saca_superficie)
    else:
        return (False, "Criterio inválido.")

    # Manejo del sentido del ordenamiento
    if orden == "desc":
        lista.reverse() # Invierte la lista para lograr un orden descendente
    elif orden != "asc":
        return (False, "Orden inválido.") # Si ingresan un texto distinto a 'asc' o 'desc' lanzamos error

    return (True, lista)


def filtro_pob(paises, pobminima, pobmaxima):
    """
    Filtra los países que estén dentro del rango de población provisto.
    """
    if not paises:
        return (False, "No hay datos cargados para filtrar.")    

    try:
        # Convertimos los límites de los rangos a enteros
        pobminima = int(pobminima)
        pobmaxima = int(pobmaxima)
    except (ValueError, TypeError):
        return (False, "Los valores de población deben ser números enteros.")

    # Validación de consistencia lógica matemática para rangos
    if pobminima > pobmaxima:
        return (False, "La población mínima no puede ser mayor que la máxima.")
        
    lista_filtrada = []
    # Evaluamos país por país comprobando que la población se ubique entre ambos extremos inclusivos
    for pais in paises:
        if pobminima <= pais["poblacion"] <= pobmaxima:
            lista_filtrada.append(pais)
            
    if not lista_filtrada:
        return (False, "No se encontraron países en ese rango de población.")
        
    return (True, lista_filtrada)


def filtro_sup(paises, supminima, supmaxima):
    """
    REQUERIMIENTO SUMADO: Filtra los países que estén dentro del 
    rango de superficie (km²) provisto.
    """
    if not paises:
        return (False, "No hay datos cargados para filtrar.")    

    try:
        # Convertimos los límites geográficos a enteros
        supminima = int(supminima)
        supmaxima = int(supmaxima)
    except (ValueError, TypeError):
        return (False, "Los valores de superficie deben ser números enteros.")

    # Validación de consistencia lógica matemática para rangos
    if supminima > supmaxima:
        return (False, "La superficie mínima no puede ser mayor que la máxima.")
        
    lista_filtrada = []
    # Evaluamos país por país comprobando que la superficie se ubique entre ambos extremos inclusivos
    for pais in paises:
        if supminima <= pais["superficie"] <= supmaxima:
            lista_filtrada.append(pais)
            
    if not lista_filtrada:
        return (False, "No se encontraron países en ese rango de superficie.")
        
    return (True, lista_filtrada)


def filtro_cont(paises, continente):
    """
    Filtra los países que pertenezcan exactamente al continente ingresado.
    """
    if not paises:
        return (False, "No hay datos cargados para filtrar.")
        
    if continente.strip() == "":
        return (False, "El continente a buscar no puede estar vacío.")
        
    lista_filtrada = []
    continente_buscado = continente.strip().lower() # Estandarizamos el término
    
    # Recorremos evaluando igualdad estricta
    for pais in paises:
        if pais["continente"] == continente_buscado:
            lista_filtrada.append(pais) # Si pertenece al continente buscado, se añade al resultado
            
    if not lista_filtrada:
        return (False, f"No se encontraron países en el continente: '{continente}'.")
        
    return (True, lista_filtrada)
