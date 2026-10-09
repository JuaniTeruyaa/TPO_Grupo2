import random

# FUNCIONES AUXILIARES Y VALIDACIONES DE CADENA / ENTRADA

def pedir_entero(mensaje):
    """Solicita al usuario una entrada y valida que sea un número entero positivo."""
    entrada = input(mensaje).strip()
    while not entrada.isdigit() or int(entrada)==0:
        print("[ERROR] El valor ingresado no es un número entero positivo válido.")
        entrada = input(mensaje).strip()
    return int(entrada)

def validar_numero(mensaje, inicio, final):
    """Valida que un número ingresado por teclado esté dentro de un rango determinado."""
    numero = pedir_entero(mensaje)
    while numero < inicio or numero > final:
        print(f"[ERROR] El número debe estar entre {inicio} y {final}.")
        numero = pedir_entero(mensaje)
    return numero

def convertidor_texto(texto):
    """Limpia un texto removiendo espacios en los extremos y convirtiéndolo a minúsculas."""
    return str(texto).strip().replace(" ", "").lower()

def validar_solo_letras(mensaje):
    """Pide un texto por teclado y asegura mediante isalpha que contenga solo caracteres alfabéticos."""
    entrada = input(mensaje).strip()
    while not entrada.replace(" ", "").isalpha():
        print("[ERROR] El nombre ingresado debe contener solo letras.")
        entrada = input(mensaje).strip()
    return entrada.title()

def validar_formato_mail(mail):
    """Verifica si el mail contiene la siguiente estructura: texto@texto.texto"""
    partes = mail.split("@")
    if len(partes) != 2:
        return False
    if partes[0] == "" or partes[1] == "":
        return False
    if "." not in partes[1]:
        return False
        
    partes_dominio = partes[1].split(".")
    es_valido = True
    
    for parte in partes_dominio:
        if parte == "":
            es_valido = False
            break 

    return es_valido


# ESTRUCTURAS INICIALES Y GENERACIÓN DE DATOS

def crear_agenda():
    """Retorna la lista de diccionarios con los contactos registrados."""
    return [
        {"id": 1, "nombre": "Juan Perez", "telefono": 123, "mail": "juan@gmail.com", "grupo": "Trabajo"},
        {"id": 2, "nombre": "Maria Gomez", "telefono": 1199887766, "mail": "maria@gmail.com", "grupo": "Familia"},
        {"id": 3, "nombre": "Lucas Silva", "telefono": 1144556677, "mail": "lucas@gmail.com", "grupo": "Amigos"},
        {"id": 4, "nombre": "Juan Silva", "telefono": 123, "mail": "lucas@gmail.com", "grupo": "Amigos"}
    ]

def crear_grupos():
    """Retorna la matriz con la definición de los grupos y su nivel de prioridad."""
    return [
        {"id":1, "nombre": "Trabajo", "descripcion": "Compañeros de la oficina y jefes", "prioridad": "Alta"},
        {"id":2, "nombre": "Familia", "descripcion": "Parientes directos y cercanos", "prioridad": "Alta"},
        {"id":3, "nombre": "Amigos", "descripcion": "Amigos del club y facultad", "prioridad": "Media"},
        {"id":4, "nombre": "Varios", "descripcion": "Contactos ocasionales", "prioridad": "Baja"}
    ]

def generar_id_unico(matriz):
    """Genera un nuevo ID numérico único evaluando el ID más alto existente."""
    max_id = max(fila["id"] for fila in matriz)
    return max_id + 1

# MENÚS DE NAVEGACIÓN Y SELECCIÓN

def menu_opciones(titulo, opciones):
    """Muestra un menú con opciones enumeradas dinámicamente usando range y retorna la selección."""
    print(f"\n=== {titulo.upper()} ===")
    for i in range(len(opciones)):
        print(f"  [{i + 1}] {opciones[i]}")
    return validar_numero(f"Seleccione una opción (1-{len(opciones)}): ", 1, len(opciones))

def seleccionar_grupo(grupos):
    """Permite al usuario seleccionar dinámicamente un grupo válido dentro de la matriz."""
    print("\n--- GRUPOS DISPONIBLES ---")
    opciones_grupos = [
        f"{grupo["nombre"]} (Prioridad: {grupo["prioridad"]}) - {grupo["descripcion"]}" 
        for grupo in grupos
    ]
    opcion = menu_opciones("Seleccionar Grupo", opciones_grupos)
    return grupos[opcion - 1]["nombre"]

# FUNCIONES DE BÚSQUEDA Y FILTRADO

def buscar_por_id(matriz):
    """Recibe un id  y valida si se encuentra en la matriz"""
    pos=-1
    dato_numero = pedir_entero("Dime el id: ")
    for i in range(len(matriz)):
        if  dato_numero == matriz[i]["id"]:
            pos=i
            break
    return pos

def buscar_por_telefono(dato, agenda):
    """Busca un contacto por número de teléfono y devuelve su índice en la matriz."""
    encontrados = list(filter(
            lambda contacto: str(dato) in str(contacto["telefono"]), 
            agenda
        ))
    return encontrados

def buscar_por_gmail(dato, agenda):
    """Busca un contacto por correo electrónico y devuelve su índice en la matriz."""
    dato_limpio = convertidor_texto(dato)
    encontrados = list(filter(
                lambda contacto: dato_limpio in convertidor_texto(contacto["mail"]), 
                agenda
            ))
    return encontrados

def buscar_por_nombre(dato, matriz):
    """Busca un contacto por correo electrónico y devuelve su índice en la matriz."""
    dato_limpio = convertidor_texto(dato)
    encontrados = list(filter(
                lambda contacto: dato_limpio in convertidor_texto(contacto["nombre"]), 
                matriz
            ))
    return encontrados

def buscar_por_grupo(dato, agenda):
    """Filtra y devuelve todos los contactos pertenecientes a un grupo."""
    dato_limpio = convertidor_texto(dato)
    encontrados = list(filter(
        lambda contacto: convertidor_texto(contacto["grupo"]) == dato_limpio, 
        agenda
    ))
    return encontrados


def buscar_grupos_por_prioridad(dato, grupos):
    """Filtra y devuelve todos los grupos que coincidan con una prioridad dada."""
    encontrados = list(filter(
        lambda grupo: grupo["prioridad"] == dato, 
        grupos
    ))
    return encontrados

# OPERACIONES ALTA, BAJA Y MODIFICACIÓN

def agregar_contacto(agenda, grupos):
    """Registra un nuevo contacto solicitando datos y asignando un ID aleatorio único."""
    print("\n=== AGREGAR NUEVO CONTACTO ===")
    nuevo_id = generar_id_unico(agenda)
    nombre = validar_solo_letras("Ingrese el nombre completo: ")
    telefono = pedir_entero("Ingrese el número de teléfono: ")
    mail = input("Ingrese el correo electrónico: ").strip().lower()
    while not validar_formato_mail(mail):
        print("[ERROR] El correo es una cadena vacia o no tiene @.")
        mail = input("Ingrese otro correo electrónico: ").strip().lower()
    grupo = seleccionar_grupo(grupos)
    
    nuevo_contacto = {
        "id": nuevo_id,
        "nombre": nombre,
        "telefono": telefono,
        "mail": mail,
        "grupo": grupo
    }
    
    agenda.append(nuevo_contacto)
    print(f"\n[ÉXITO] Contacto '{nombre}' agregado con éxito (ID asignado: {nuevo_id}).")

def agregar_grupo(grupos):
    """Registra un nuevo grupo solicitando datos y asignando un ID aleatorio único."""
    print("\n=== AGREGAR NUEVO GRUPO ===")
    nuevo_id = generar_id_unico(grupos)
    nombre = validar_solo_letras("Ingrese el nombre: ")
    descripcion = input("Ingrese la descripcion del grupo: ").strip()
    opciones_prioridades = ["Alta", "Media", "Baja"]
    eleccion_prio = menu_opciones("Prioridad", opciones_prioridades)
    valor = opciones_prioridades[eleccion_prio - 1]
    prioridad=valor
    
    nuevo_grupo = {
        "id": nuevo_id,
        "nombre": nombre,
        "descripcion": descripcion,
        "prioridad": prioridad
    }
    grupos.append(nuevo_grupo)
    print(f"\n[ÉXITO] Grupo '{nombre}' agregado con éxito (ID asignado: {nuevo_id}).")

def cambiar_dato(matriz, pos, nuevo_valor, clave):
    """Aplica la modificación in situ sobre la matriz de agenda."""
    matriz[pos][clave] = nuevo_valor
    print("[ÉXITO] Contacto modificado correctamente.")
    
def modificar_contacto(agenda, pos, grupos):
    """Muestra las opciones de modificar contacto y ejecuta el cambio"""
    opciones_modificar = ["Nombre", "Teléfono", "Mail", "Grupo", "Cancelar"]
    eleccion = menu_opciones("Menú de Modificación", opciones_modificar)
    match eleccion:
        case 1:
            valor = validar_solo_letras("Dime el nuevo nombre: ")
            cambiar_dato(agenda, pos, valor, "nombre")
        case 2:
            valor = pedir_entero("Dime el nuevo teléfono: ")
            cambiar_dato(agenda, pos, valor, "telefono")
        case 3:
            valor = input("Dime el nuevo mail: ").strip().lower()
            while not validar_formato_mail(valor):
                print("[ERROR] El correo  es una cadena vacia o no tiene @.")
                valor = input("Dime el nuevo mail: ").strip().lower()
            cambiar_dato(agenda, pos, valor, "mail")
        case 4:
            id_grupo = seleccionar_grupo(grupos)
            cambiar_dato(agenda, pos, id_grupo, "grupo")
        case 5:
            print("[INFO] Operación cancelada.")
            
def modificar_grupo(agenda, pos, grupos):
    opciones_modificar_grupo = ["Nombre del grupo", "Descripción", "Prioridad", "Cancelar"]
    eleccion = menu_opciones("Menú de Modificación de Grupo", opciones_modificar_grupo)
    match eleccion:
        case 1:
            nombre_anterior = grupos[pos]["nombre"]
            valor = validar_solo_letras("Dime el nuevo nombre: ")
            cambiar_dato(grupos, pos, valor.title(), 1)
            for contacto in agenda:
                if convertidor_texto(contacto["grupo"]) == convertidor_texto(nombre_anterior):
                    contacto["grupo"] = valor
        case 2:
            valor = input("Dime la nueva descripción del grupo: ").strip()
            cambiar_dato(grupos, pos, valor, "descripcion")
        case 3:
            prioridades = ["Alta", "Media", "Baja"]
            print("\n--- SELECCIONAR NUEVA PRIORIDAD ---")
            eleccion_prio = menu_opciones("Prioridad", prioridades)
            valor = prioridades[eleccion_prio - 1]
            cambiar_dato(grupos, pos, valor, "prioridad")
        case 4:
            print("[INFO] Operación cancelada.")



def eliminar(matriz):
    """Busca y elimina una persona de la lista usando pop."""
    pos = buscar_por_id(matriz)
    if pos == -1:
        print("[RESULTADO] Error al encontrarlo/a.")
    else:
        eliminado = matriz.pop(pos)
        print(f"[ÉXITO] '{eliminado["nombre"]}' eliminado correctamente.")

def eliminar_grupo(grupos, agenda):
    """Elimina un grupo y reasigna sus contactos al grupo 'Varios'."""
    pos = buscar_por_id(grupos)
    if pos == -1:
        print("[RESULTADO] Error: Grupo no encontrado.")
    else:
        nombre_grupo = grupos[pos]["nombre"]
        if convertidor_texto(nombre_grupo) == "varios":
            print("[ERROR] No se puede eliminar el grupo por defecto 'Varios'.")
            
        else:
            grupos.pop(pos)
            for contacto in agenda:
                if convertidor_texto(contacto["grupo"]) == convertidor_texto(nombre_grupo):
                    contacto["grupo"] = "Varios"
            print(f"[ÉXITO] Grupo '{nombre_grupo}' eliminado. Sus contactos pasaron a 'Varios'.")

# VISUALIZACIÓN

def mostrar_contacto(contacto):
    """Muestra la ficha detallada de un contacto accediendo por clave."""
    id_fmt = str(contacto["id"]).zfill(4)
    print(f"ID: {id_fmt:<5} | Nombre: {contacto['nombre']:<18} | Tel: {contacto['telefono']:<12} | Mail: {contacto['mail']:<20} | Grupo: {contacto['grupo']:<10}")
    
def mostrar_grupo(grupo):
    """Muestra la ficha detallada de un grupo accediendo por clave."""
    id_grupo = str(grupo["id"]).zfill(4)
    print(f"ID: {id_grupo:<5} | Grupo: {grupo['nombre']:<15} | Descripción: {grupo['descripcion']:<35} | Prioridad: {grupo['prioridad']:<10}")
    
def mostrar_matriz_formateada(titulo, datos, cabeceras):
    """Imprime cualquier matriz en formato tabla asegurando ancho uniforme con rebanadas."""
    linea_cabecera = " | ".join([f"{h:^20}" for h in cabeceras])
    print(f"\n{titulo.upper().center(len(linea_cabecera),'-')}")
    print("=" * len(linea_cabecera))
    print(linea_cabecera)
    print("=" * len(linea_cabecera))
    
    for fila in datos:
        fila_str = [str(elem)[:20] for elem in fila]
        fila_str[0] = fila_str[0].zfill(4)
        print(" | ".join([f"{col:<20}" for col in fila_str]))
    print("=" * len(linea_cabecera))

def mostrar(agenda, grupos):
    """Muestra las tablas ordenadas de contactos y grupos."""
    agenda_ordenada = sorted(agenda, key=lambda c: c["nombre"])
    filas_agenda = [
        [c["id"], c["nombre"], c["telefono"], c["mail"], c["grupo"]] 
        for c in agenda_ordenada
    ]
    cabeceras_contacto = ["ID", "Nombre", "Teléfono", "Mail", "Grupo"]
    mostrar_matriz_formateada("Contactos (Ordenados por Nombre)", filas_agenda, cabeceras_contacto)

    filas_grupos = [
        [g["id"], g["nombre"], g["descripcion"], g["prioridad"]] 
        for g in grupos
    ]
    cabeceras_grupo = ["ID", "Nombre Grupo", "Descripción", "Prioridad"]
    mostrar_matriz_formateada("Grupos", filas_grupos, cabeceras_grupo)
    
def mostrar_en_busqueda(encontrados,dato):
    """Muestra los resultados de la busqueda"""
    if len(encontrados) == 0:
        print(f"\n[RESULTADO] No hay contactos registrados con '{dato}'.")
    else:
        print(f"\n[RESULTADO] Contactos encontrados con '{dato}' ({len(encontrados)}):")
        for contacto in encontrados:
            mostrar_contacto(contacto)
    

def eleccion_de_busqueda_contactos(agenda, grupos):
    """Gestor de sub-menú para realizar búsquedas por distintos parámetros mediante match-case."""
    opciones_busqueda = [
        "Buscar por ID",
        "Buscar por nombre",
        "Buscar por número de teléfono",
        "Buscar por grupo",
        "Buscar por mail",
        "Volver al menú principal"
    ]
    
    forma_de_busqueda = menu_opciones("Opciones de Búsqueda", opciones_busqueda)

    match forma_de_busqueda:
        case 1:
            pos = buscar_por_id(agenda)
            if pos == -1:
                print("\n[RESULTADO] Contacto no encontrado.")
            else:
                print("\n[RESULTADO] Contacto encontrado:")
                mostrar_contacto(agenda[pos])
                
        case 2:
            dato=input("Ingresar el nombre o parte de este: ").strip()
            encontrados = buscar_por_nombre(dato, agenda)
            mostrar_en_busqueda(encontrados,dato)
            
            
        case 3:
            dato=pedir_entero("Ingresar el numero de telefono o parte de este:")
            encontrados = buscar_por_telefono(dato, agenda)
            mostrar_en_busqueda(encontrados,dato)
            
        case 4:
            dato = seleccionar_grupo(grupos)
            encontrados = buscar_por_grupo(dato, agenda)
            mostrar_en_busqueda(encontrados,dato)
            
            
        case 5:
            dato=input("Ingresar el mail o parte de este: ").strip()
            encontrados = buscar_por_gmail(dato, agenda)
            mostrar_en_busqueda(encontrados,dato)
            
        case 6:
            print("[INFO] Regresando al menú principal...")

def eleccion_de_busqueda_grupos(grupos):
    """Gestor de sub-menú para realizar búsquedas de grupos por distintos parámetros mediante match-case."""
    opciones_busqueda = [
        "Buscar grupo por ID",
        "Buscar grupo por nombre",
        "Buscar grupos por nivel de prioridad",
        "Volver al menú principal"
    ]
    
    forma_de_busqueda = menu_opciones("Opciones de Búsqueda de Grupos", opciones_busqueda)

    match forma_de_busqueda:
        case 1:
            pos = buscar_por_id(grupos)
            if pos == -1:
                print("\n[RESULTADO] Grupo no encontrado.")
            else:
                print("\n[RESULTADO] Grupo encontrado:")
                mostrar_grupo(grupos[pos])
                
        case 2:
            dato=input("Ingresar el nombre o parte de este: ").strip()
            encontrados = buscar_por_nombre(dato, grupos)
            if len(encontrados) == 0:
                    print(f"\n[RESULTADO] No hay Grupos registrados con '{dato}'.")
            else:
                print(f"\n[RESULTADO] Grupos encontrados con '{dato}' ({len(encontrados)}):")
                for grupo in encontrados:
                    mostrar_grupo(grupo)
            
        case 3:
            prioridades = ["Alta", "Media", "Baja"]
            print("\n--- SELECCIONAR PRIORIDAD A BUSCAR ---")
            eleccion_prio = menu_opciones("Prioridad", prioridades)
            dato = prioridades[eleccion_prio - 1]
            
            encontrados = buscar_grupos_por_prioridad(dato, grupos)
            if len(encontrados) == 0:
                print(f"\n[RESULTADO] No hay grupos registrados con prioridad '{dato}'.")
            else:
                print(f"\n[RESULTADO] Grupos encontrados con prioridad '{dato}' ({len(encontrados)}):")
                for grupo in encontrados:
                    mostrar_grupo(grupo)
            
        case 4:
            print("[INFO] Regresando al menú principal...")

# FUNCIÓN PRINCIPAL

def main():
    """Función principal que coordina el flujo global de la aplicación."""
    agenda = crear_agenda()
    grupos = crear_grupos()
    ejecutando = True
    
    opciones_main = [
        "Agregar un contacto",
        "Modificar un contacto",
        "Eliminar un contacto",
        "Eliminar un grupo",
        "Ver todos los contactos y grupos",
        "Buscar contacto",
        "Modificar un grupo",
        "Buscar un grupo",
        "Agregar un grupo",
        "Salir"
    ]
    
    while ejecutando:
        eleccion = menu_opciones("Agenda de Contactos", opciones_main)
        
        match eleccion:
            case 1:
                agregar_contacto(agenda, grupos)
            case 2:
                pos = buscar_por_id(agenda)
                if pos == -1:
                    print("[RESULTADO] Persona no encontrada.")
                else:
                    modificar_contacto(agenda, pos, grupos)
            case 3:
                eliminar(agenda)
            case 4:
                eliminar_grupo(grupos, agenda)
            case 5:
                mostrar(agenda, grupos)
            case 6:
                eleccion_de_busqueda_contactos(agenda, grupos)
            case 7:
                posGrupo = buscar_por_id(grupos)
                if posGrupo == -1:
                    print("[RESULTADO] Grupo no encontrado.")
                else:
                    modificar_grupo(agenda, posGrupo, grupos)
            case 8: 
                eleccion_de_busqueda_grupos(grupos)

            case 9:
                agregar_grupo(grupos)
            
            case 10:
                print("\n¡Gracias por usar la agenda! Saliendo...")
                ejecutando = False
            


main()