import csv



# Levanta el csv, pide la ruta y prepara la lista de diccionarios "paises" para retornarla si todo sale bien.
def cargar_csv(ruta):
    paises = []

    try:
        with open(ruta, newline='', encoding='utf-8') as archivo:
            lector = csv.DictReader(archivo)

            for fila in lector:
                try:
                    if not fila.get("nombre") or not fila.get("poblacion") or not fila.get("superficie") or not fila.get("continente"):
                        continue

                    pais = {
                        "nombre": fila["nombre"].strip().lower(),
                        "poblacion": int(fila["poblacion"]),
                        "superficie": int(fila["superficie"]),
                        "continente": fila["continente"].strip().lower()
                    }

                    paises.append(pais)

                except:
                    continue

    except FileNotFoundError:
        return []

    return paises

#escribe la lista de paises desde 0 con la lista trabajada como recurso, solo retorna true pero habiendo escrito en el csv.
def guardar_csv(ruta, paises):
    if not paises:
        return False 
    
    encabezados = ["nombre", "poblacion", "superficie", "continente"]
    try:
        with open(ruta, "w", newline='', encoding='utf-8') as archivo:
            paquete = csv.DictWriter(archivo, fieldnames=encabezados)
            paquete.writeheader() 
            
            paises_formateados = [] 
            for p in paises:
                p_formato = {
                    "nombre": p["nombre"].capitalize(),
                    "poblacion": p["poblacion"],
                    "superficie": p["superficie"],
                    "continente": p["continente"].capitalize()
                }
                paises_formateados.append(p_formato)
            
            paquete.writerows(paises_formateados) 
            return True 
    except Exception:
        return False

#Valida que lo que ingresas como nuevo sea un diccionario que responden a los encabezados correspondientes.
def validar_estructura(nuevo):
    if not isinstance(nuevo, dict):
        return (False, "El dato a ingresar no es del formato adecuado.")
    
    for llave in ["nombre", "poblacion", "superficie", "continente"]:
        if llave not in nuevo or nuevo[llave] is None:
            return (False, f"El dato a ingresar no está completo. Falta el campo '{llave}'.")
    return (True, "Validación exitosa")

# Valida que las claves a agregar del diccionario nuevo tengan COHERENCIA con la estructura del proyecto.
def validar_datos(nuevo):
    if not isinstance(nuevo["nombre"], str) or nuevo["nombre"].strip() == "":
        return (False, "Nombre inválido.")

    try:
        if int(nuevo["poblacion"]) <= 0:
            return (False, "Población inválida. Debe ser un número entero positivo.")
    except (ValueError, TypeError):
        return (False, "Población inválida. Debe ser un número entero positivo.")

    try:
        if int(nuevo["superficie"]) <= 0:
            return (False, "Superficie inválida. Debe ser un número entero positivo.")
    except (ValueError, TypeError):
        return (False, "Superficie inválida. Debe ser un número entero positivo.")

    if not isinstance(nuevo["continente"], str) or nuevo["continente"].strip() == "":
        return (False, "Continente inválido.")
    
    return (True, "Validación exitosa")

#Chequea si ya existe el pais buscado, mas que nada para comparar y usarla como funcion auxiliar en las que lo requieran.
def ya_existe_pais(nombre_pais, paises):
    nombre_buscado = str(nombre_pais).strip().lower() 
    for item in paises:
        if nombre_buscado == item["nombre"]:
            return True 
    return False 

#Recibe el nuevo pais, valida datos, evita duplicados y lo agrega a la lista si es valido
def agregar_pais(nuevo, paises):
    valido, mensaje = validar_estructura(nuevo)
    if not valido:
        return (False, mensaje)

    valido, mensaje = validar_datos(nuevo)
    if not valido:
        return (False, mensaje)
    
    if ya_existe_pais(nuevo["nombre"], paises):
        return (False, "El país que quiere agregar ya se encuentra en la base de datos.")

    linea_nueva = {
        "nombre": nuevo["nombre"].strip().lower(), 
        "poblacion": int(nuevo["poblacion"]),
        "superficie": int(nuevo["superficie"]),
        "continente": nuevo["continente"].strip().lower()
    }
    paises.append(linea_nueva) 
    return (True, "País agregado correctamente.")

#Recibe el nombre para encontrarlo, si lo encuentra, usa los argumentos de nuevapob/nuevasup y son validados, actualiza su poblacion y superficie.
def modificar_pais(cual, paises, nuevapob, nuevasup):
    if not ya_existe_pais(cual, paises):
        return (False, "El país ingresado para modificar no se encuentra registrado previamente.")

    try:
        nuevapob = int(nuevapob)
        nuevasup = int(nuevasup)
    except (ValueError, TypeError):
        return (False, "Los datos ingresados para población o superficie no son del tipo adecuado.")


    if nuevapob <= 0 or nuevasup <= 0:
        return (False, "Los datos ingresados para población o superficie deben ser positivos.")
    
    cual_buscado = cual.strip().lower() 


    for item in paises:
        if cual_buscado == item["nombre"]:
            item["poblacion"] = nuevapob  
            item["superficie"] = nuevasup 
            break 

    return (True, "El país fue modificado correctamente.")

#Recibe un string, lo estandariza, se fija a cuales paises referencia aunque sea parcialmente, y arma una lista, devuelve el resultado en un string largo.
def buscador(cual, paises):
    coinciden = [] 
    cual = cual.lower().strip() 
    if not cual:
        return (False, "Ingrese un nombre de país válido.")


    for item in paises:
        if cual in item["nombre"]:
            coinciden.append(item) 

    if not coinciden:
        return (False, "El país ingresado no se encuentra en la base de datos.")

    lista_mensajes = [f"Tu palabra ingresada '{cual}' tiene {len(coinciden)} de coincidencia/s:"]
    for item in coinciden:
        mensaje = f"{item['nombre'].capitalize()} | población: {item['poblacion']} | superficie: {item['superficie']} km² | continente: {item['continente'].capitalize()}."
        lista_mensajes.append(mensaje)

    resultado = "\n".join(lista_mensajes) 
    return (True, resultado)


#Recorre la lista, calcula max, min, promedios y conteo por continente, arma el reporte y lo retorna.
def estadistica(paises):
    if not paises:
        return (False, "No hay datos cargados.")


    primero = paises[0]
    mas_poblado = primero
    menos_poblado = primero
    pob_promedio = 0    
    sup_promedio = 0    
    conteo_continentes = {} 

    for item in paises:
        pob_promedio += item["poblacion"]   
        sup_promedio += item["superficie"] 

        if item["poblacion"] > mas_poblado["poblacion"]:
            mas_poblado = item

        if item["poblacion"] < menos_poblado["poblacion"]:
            menos_poblado = item
            
        cont = item["continente"].capitalize()
        if cont in conteo_continentes:
            conteo_continentes[cont] += 1 
        else:
            conteo_continentes[cont] = 1  


    pob_promedio = pob_promedio / len(paises)
    sup_promedio = sup_promedio / len(paises)


    lineas_continentes = []
    for cont, cant in conteo_continentes.items():
        lineas_continentes.append(f" - {cont}: {cant} país/es")
    texto_continentes = "\n".join(lineas_continentes)


    mensaje = f'''El país más poblado es {mas_poblado["nombre"].capitalize()}, con {mas_poblado["poblacion"]} habitantes.
El país menos poblado es {menos_poblado["nombre"].capitalize()}, con {menos_poblado["poblacion"]} habitantes.
El promedio total de la población según los países cargados es de: {round(pob_promedio)} habitantes por país.
El promedio de la superficie de entre todos los países cargados es de: {round(sup_promedio)} km².

Cantidad de países por continente:
{texto_continentes}'''
    
    return (True, mensaje)


# Funciones auxiliares requeridas por SORTED() para extraer las llaves de ordenamiento
def saca_nombre(p): 
    return p["nombre"]

def saca_poblacion(p): 
    return p["poblacion"]

def saca_superficie(p): 
    return p["superficie"]

#Ordena los paises segun criterio y orden usando sorted y funciones auxiliares
def ordenar_paises(paises, criterio, orden):
    if not paises:
        return (False, "No hay datos cargados.")

    if criterio == "nombre":
        lista = sorted(paises, key=saca_nombre)
    elif criterio == "poblacion":
        lista = sorted(paises, key=saca_poblacion)
    elif criterio == "superficie":
        lista = sorted(paises, key=saca_superficie)
    else:
        return (False, "Criterio inválido.")


    if orden == "desc":
        lista.reverse() 
    elif orden != "asc":
        return (False, "Orden inválido.") 

    return (True, lista)


#Recibe los argumentos que necesita, los filtra y arma lista con los elementos dentro del rango requerido (POBLACION).
def filtro_pob(paises, pobminima, pobmaxima):

    if not paises:
        return (False, "No hay datos cargados para filtrar.")    

    try:
        pobminima = int(pobminima)
        pobmaxima = int(pobmaxima)
    except (ValueError, TypeError):
        return (False, "Los valores de población deben ser números enteros.")

    if pobminima > pobmaxima:
        return (False, "La población mínima no puede ser mayor que la máxima.")
        
    lista_filtrada = []
    for pais in paises:
        if pobminima <= pais["poblacion"] <= pobmaxima:
            lista_filtrada.append(pais)
            
    if not lista_filtrada:
        return (False, "No se encontraron países en ese rango de población.")
        
    return (True, lista_filtrada)


#Recibe los argumentos que necesita, los filtra y arma lista con los elementos dentro del rango requerido (SUPERFICIE).
def filtro_sup(paises, supminima, supmaxima):
    if not paises:
        return (False, "No hay datos cargados para filtrar.")    

    try:
        supminima = int(supminima)
        supmaxima = int(supmaxima)
    except (ValueError, TypeError):
        return (False, "Los valores de superficie deben ser números enteros.")

    if supminima > supmaxima:
        return (False, "La superficie mínima no puede ser mayor que la máxima.")
        
    lista_filtrada = []
    for pais in paises:
        if supminima <= pais["superficie"] <= supmaxima:
            lista_filtrada.append(pais)
            
    if not lista_filtrada:
        return (False, "No se encontraron países en ese rango de superficie.")
        
    return (True, lista_filtrada)

#Recibe el continente a filtrar y devuelve una lista con los paises que pertenecen a el
def filtro_cont(paises, continente):
    if not paises:
        return (False, "No hay datos cargados para filtrar.")
        
    if continente.strip() == "":
        return (False, "El continente a buscar no puede estar vacío.")
        
    lista_filtrada = []
    continente_buscado = continente.strip().lower() 
    
    for pais in paises:
        if pais["continente"] == continente_buscado:
            lista_filtrada.append(pais) 
            
    if not lista_filtrada:
        return (False, f"No se encontraron países en el continente: '{continente}'.")
        
    return (True, lista_filtrada)
