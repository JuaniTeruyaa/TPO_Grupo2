import random

# ==============================================================================
# FUNCIONES AUXILIARES Y VALIDACIONES DE CADENA / ENTRADA
# ==============================================================================

def pedir_entero(mensaje):
    """Solicita al usuario una entrada y valida que sea un número entero positivo."""
    entrada = input(mensaje).strip()
    while not entrada.isdigit():
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

def validar_repetido(valor, matriz, columna):
    """Verifica si el valor ya esta en la matriz"""
    for i in range(len(matriz)):
        if convertidor_texto(matriz[i][columna]) == convertidor_texto(valor):
            return True
    return False

# ==============================================================================
# ESTRUCTURAS INICIALES Y GENERACIÓN DE DATOS
# ==============================================================================

def crear_agenda():
    """Retorna la matriz inicial con los contactos registrados."""
    return [
        [1, "Juan Perez", 1122334455, "juan@gmail.com", "Trabajo"],
        [2, "Maria Gomez", 1199887766, "maria@gmail.com", "Familia"],
        [3, "Lucas Silva", 1144556677, "lucas@gmail.com", "Amigos"]
    ]

def crear_grupos():
    """Retorna la matriz con la definición de los grupos y su nivel de prioridad."""
    return [
        [1, "Trabajo", "Compañeros de la oficina y jefes", "Alta"],
        [2, "Familia", "Parientes directos y cercanos", "Alta"],
        [3, "Amigos", "Amigos del club y facultad", "Media"],
        [4, "Varios", "Contactos ocasionales", "Baja"]
    ]

def generar_id_unico(matriz):
    """Genera un nuevo ID numérico aleatorio único que no colisione con existentes."""
    ids_existentes = [particular[0] for particular in matriz]
    nuevo_id = random.randint(100, 999)
    while nuevo_id in ids_existentes:
        nuevo_id = random.randint(100, 999)
    return nuevo_id

# ==============================================================================
# MENÚS DE NAVEGACIÓN Y SELECCIÓN
# ==============================================================================

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
        f"{grupo[1]} (Prioridad: {grupo[3]}) - {grupo[2]}" 
        for grupo in grupos
    ]
    opcion = menu_opciones("Seleccionar Grupo", opciones_grupos)
    return grupos[opcion - 1][1]

# ==============================================================================
# FUNCIONES DE BÚSQUEDA Y FILTRADO (Uso de range)
# ==============================================================================

def buscar_por_nombre_o_id(dato, matriz):
    """Busca por ID o Nombre y devuelve su posición/índice en la matriz."""
    dato_limpio = convertidor_texto(dato)
    for i in range(len(matriz)):
        id = str(matriz[i][0])
        nom = convertidor_texto(matriz[i][1])
        if dato_limpio == id or dato_limpio == nom:
            return i
    return -1

def buscar_por_telefono(dato, agenda):
    """Busca un contacto por número de teléfono y devuelve su índice en la matriz."""
    for j in range(len(agenda)):
        if agenda[j][2] == dato:
            return j
    return -1

def buscar_por_gmail(dato, agenda):
    """Busca un contacto por correo electrónico y devuelve su índice en la matriz."""
    dato_limpio = convertidor_texto(dato)
    for l in range(len(agenda)):
        if convertidor_texto(agenda[l][3]) == dato_limpio:
            return l
    return -1

def buscar_por_grupo(dato, agenda):
    """Filtra y devuelve todos los contactos pertenecientes a un grupo."""
    dato_limpio = convertidor_texto(dato)
    encontrados = list(filter(
        lambda contacto: convertidor_texto(contacto[4]) == dato_limpio, 
        agenda
    ))
    return encontrados


def buscar_grupos_por_prioridad(dato, grupos):
    """Filtra y devuelve todos los grupos que coincidan con una prioridad dada."""
    encontrados = list(filter(
        lambda grupo: grupo[3] == dato, 
        grupos
    ))
    return encontrados
# ==============================================================================
# OPERACIONES ALTA, BAJA Y MODIFICACIÓN
# ==============================================================================

def agregar_contacto(agenda, grupos):
    """Registra un nuevo contacto solicitando datos y asignando un ID aleatorio único."""
    print("\n=== AGREGAR NUEVO CONTACTO ===")
    nuevo_id = generar_id_unico(agenda)
    nombre = validar_solo_letras("Ingrese el nombre completo: ")
    while validar_repetido(nombre,agenda,1):
        nombre = validar_solo_letras("No se puede repetir el nombre: ")
    telefono = pedir_entero("Ingrese el número de teléfono: ")
    while validar_repetido(telefono,agenda,2):
        print("[ERROR] El teléfono ya está registrado.")
        telefono = pedir_entero("Ingrese otro número de teléfono: ")
    mail = input("Ingrese el correo electrónico: ").strip().lower()
    while validar_repetido(mail,agenda,3):
        print("[ERROR] El correo ya está registrado.")
        mail = input("Ingrese otro correo electrónico: ").strip().lower()
    grupo = seleccionar_grupo(grupos)
    
    nuevo_contacto = [nuevo_id, nombre, telefono, mail, grupo]
    agenda.append(nuevo_contacto)
    print(f"\n[ÉXITO] Contacto '{nombre}' agregado con éxito (ID asignado: {nuevo_id}).")

def agregar_grupo(grupos):
    """Registra un nuevo grupo solicitando datos y asignando un ID aleatorio único."""
    print("\n=== AGREGAR NUEVO GRUPO ===")
    nuevo_id = generar_id_unico(grupos)
    nombre = validar_solo_letras("Ingrese el nombre: ")
    while validar_repetido(nombre,grupos,1):
            nombre = validar_solo_letras("No se puede repetir el nombre: ")
    descripcion = input("Ingrese la descripcion del grupo: ").strip()
    opciones_prioridades = ["Alta", "Media", "Baja"]
    eleccion_prio = menu_opciones("Prioridad", opciones_prioridades)
    valor = opciones_prioridades[eleccion_prio - 1]
    prioridad=valor
    
    nuevo_grupo = [nuevo_id, nombre, descripcion, prioridad]
    grupos.append(nuevo_grupo)
    print(f"\n[ÉXITO] Grupo '{nombre}' agregado con éxito (ID asignado: {nuevo_id}).")

def cambiar_dato(matriz, pos, nuevo_valor, columna):
    """Aplica la modificación in situ sobre la matriz de agenda."""
    matriz[pos][columna] = nuevo_valor
    print("[ÉXITO] Contacto modificado correctamente.")

def modificar(agenda, pos, grupos, categoria):
    """Despliega las opciones de modificación e impacta el cambio según corresponda."""
    
    if categoria == 0:

        opciones_modificar = ["Nombre", "Teléfono", "Mail", "Grupo", "Cancelar"]
        eleccion = menu_opciones("Menú de Modificación", opciones_modificar)

        match eleccion:
            case 1:
                valor = validar_solo_letras("Dime el nuevo nombre: ")
                while validar_repetido(valor,agenda,1):
                    valor = validar_solo_letras("No se puede repetir el nombre: ")
                cambiar_dato(agenda, pos, valor, 1)
            case 2:
                valor = pedir_entero("Dime el nuevo teléfono: ")
                while validar_repetido(valor,agenda,2):
                    valor = pedir_entero("No se puede repetir el numero: ")
                cambiar_dato(agenda, pos, valor, 2)
            case 3:
                valor = input("Dime el nuevo mail: ").strip().lower()
                while validar_repetido(valor,agenda,3):
                    valor = validar_solo_letras("No se puede repetir el mail: ")
                cambiar_dato(agenda, pos, valor, 3)
            case 4:
                id_grupo = seleccionar_grupo(grupos)
                cambiar_dato(agenda, pos, id_grupo, 4)
            case 5:
                print("[INFO] Operación cancelada.")
    else: 

        opciones_modificar_grupo = ["Nombre del grupo", "Descripción", "Prioridad", "Cancelar"]
        eleccion = menu_opciones("Menú de Modificación de Grupo", opciones_modificar_grupo)
        
        match eleccion:
            case 1:
                valor = validar_solo_letras("Dime el nuevo nombre: ")
                while validar_repetido(valor,grupos,1):
                    valor = validar_solo_letras("No se puede repetir el nombre: ")
                cambiar_dato(grupos, pos, valor, 1)
            case 2:
                valor = input("Dime la nueva descripción del grupo: ").strip()
                cambiar_dato(grupos, pos, valor, 2)
            case 3:
                prioridades = ["Alta", "Media", "Baja"]
                print("\n--- SELECCIONAR NUEVA PRIORIDAD ---")
                eleccion_prio = menu_opciones("Prioridad", prioridades)
                valor = prioridades[eleccion_prio - 1]
                cambiar_dato(grupos, pos, valor, 3)
            case 4:
                print("[INFO] Operación cancelada.")


def eliminar(matriz):
    """Busca y elimina una persona de la lista usando pop."""
    data = input("Dime el nombre/id de lo que quieres eliminar: ").strip()
    pos = buscar_por_nombre_o_id(data, matriz)
    if pos == -1:
        print("[RESULTADO] Error al encontrarlo/a.")
    else:
        eliminado = matriz.pop(pos)
        print(f"[ÉXITO] '{eliminado[1]}' eliminado correctamente.")

# ==============================================================================
# VISUALIZACIÓN
# ==============================================================================

def mostrar_contacto(contacto):
    """Muestra la ficha detallada de un contacto utilizando marcadores de posición f-string."""
    id = str(contacto[0]).zfill(4)
    print(f"ID: {id:<5} | Nombre: {contacto[1]:<18} | Tel: {contacto[2]:<12} | Mail: {contacto[3]:<20} | Grupo: {contacto[4]:<10}")

def mostrar_grupo(grupo):
    """Muestra la ficha detallada de un grupo utilizando marcadores de posición f-string."""
    id_grupo = str(grupo[0]).zfill(4)
    print(f"ID: {id_grupo:<5} | Grupo: {grupo[1]:<15} | Descripción: {grupo[2]:<35} | Prioridad: {grupo[3]:<10}")
    
def mostrar_matriz_formateada(titulo, datos, cabeceras):
    """Imprime cualquier matriz en formato tabla asegurando ancho uniforme con rebanadas."""
    linea_cabecera = " | ".join([f"{h:^20}" for h in cabeceras])
    print(f"\n{titulo.upper().center(len(linea_cabecera),"-")}")
    print("=" * len(linea_cabecera))
    print(linea_cabecera)
    print("=" * len(linea_cabecera))
    
    for fila in datos:
        fila_str = [str(elem)[:20] for elem in fila]
        fila_str[0] = fila_str[0].zfill(4)
        print(" | ".join([f"{col:<20}" for col in fila_str]))
    print("=" * len(linea_cabecera))

def mostrar(agenda, grupos):
    """Muestra las tablas ordenadas de contactos y grupos utilizando."""
    agenda_ordenada = sorted(agenda, key=lambda c: c[0])
    cabeceras_contacto = ["ID", "Nombre", "Teléfono", "Mail", "Grupo"]
    mostrar_matriz_formateada("Contactos (Ordenados por id)", agenda_ordenada, cabeceras_contacto)

    cabeceras_grupo = ["ID", "Nombre Grupo", "Descripción", "Prioridad"]
    mostrar_matriz_formateada("Grupos", grupos, cabeceras_grupo)

def eleccion_de_busqueda_contactos(agenda, grupos):
    """Gestor de sub-menú para realizar búsquedas por distintos parámetros mediante match-case."""
    opciones_busqueda = [
        "Buscar por nombre o ID",
        "Buscar por número de teléfono",
        "Buscar por grupo",
        "Buscar por mail",
        "Volver al menú principal"
    ]
    
    forma_de_busqueda = menu_opciones("Opciones de Búsqueda", opciones_busqueda)

    match forma_de_busqueda:
        case 1:
            dato = input("Ingresar nombre o ID a buscar: ").strip()
            pos = buscar_por_nombre_o_id(dato, agenda)
            if pos == -1:
                print("\n[RESULTADO] Contacto no encontrado.")
            else:
                print("\n[RESULTADO] Contacto encontrado:")
                mostrar_contacto(agenda[pos])
            
        case 2:
            dato = pedir_entero("Ingresar número de teléfono: ")
            pos = buscar_por_telefono(dato, agenda)
            if pos == -1:
                print("\n[RESULTADO] Contacto no encontrado.")
            else:
                print("\n[RESULTADO] Contacto encontrado:")
                mostrar_contacto(agenda[pos])
            
        case 3:
            dato = seleccionar_grupo(grupos)
            encontrados = buscar_por_grupo(dato, agenda)
            if len(encontrados) == 0:
                print(f"\n[RESULTADO] No hay contactos registrados en el grupo '{dato}'.")
            else:
                print(f"\n[RESULTADO] Contactos encontrados en el grupo '{dato}' ({len(encontrados)}):")
                for contacto in encontrados:
                    mostrar_contacto(contacto)
            
        case 4:
            dato = input("Ingresar mail: ").strip()
            pos = buscar_por_gmail(dato, agenda)
            if pos == -1:
                print("\n[RESULTADO] Contacto no encontrado.")
            else:
                print("\n[RESULTADO] Contacto encontrado:")
                mostrar_contacto(agenda[pos])
            
        case 5:
            print("[INFO] Regresando al menú principal...")

def eleccion_de_busqueda_grupos(grupos):
    """Gestor de sub-menú para realizar búsquedas de grupos por distintos parámetros mediante match-case."""
    opciones_busqueda = [
        "Buscar grupo por nombre o ID",
        "Buscar grupos por nivel de prioridad",
        "Volver al menú principal"
    ]
    
    forma_de_busqueda = menu_opciones("Opciones de Búsqueda de Grupos", opciones_busqueda)

    match forma_de_busqueda:
        case 1:
            dato = input("Ingresar nombre o ID del grupo a buscar: ").strip()
            pos = buscar_por_nombre_o_id(dato, grupos)
            if pos == -1:
                print("\n[RESULTADO] Grupo no encontrado.")
            else:
                print("\n[RESULTADO] Grupo encontrado:")
                mostrar_grupo(grupos[pos])
            
        case 2:
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
            
        case 3:
            print("[INFO] Regresando al menú principal...")
# ==============================================================================
# FUNCIÓN PRINCIPAL
# ==============================================================================

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
                dato = input("Dime el nombre de la persona que quieres modificar o su id: ").strip()
                pos = buscar_por_nombre_o_id(dato, agenda)
                if pos == -1:
                    print("[RESULTADO] Persona no encontrada.")
                else:
                    categoria = 0
                    modificar(agenda, pos, grupos, categoria)
            case 3:
                eliminar(agenda)
            case 4:
                eliminar(grupos)
            case 5:
                mostrar(agenda, grupos)
            case 6:
                eleccion_de_busqueda_contactos(agenda, grupos)
            case 7:
                datoGrupo = input("Dime el nombre del grupo que quieres modificar o su id: ").strip()
                posGrupo = buscar_por_nombre_o_id(datoGrupo, grupos)
                if posGrupo == -1:
                    print("[RESULTADO] Grupo no encontrado.")
                else:
                    categoria = 1
                    modificar(agenda, posGrupo, grupos, categoria)
            case 8: 
                eleccion_de_busqueda_grupos(grupos)

            case 9:
                agregar_grupo(grupos)
            
            case 10:
                print("\n¡Gracias por usar la agenda! Saliendo...")
                ejecutando = False
            


main()