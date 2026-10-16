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
    while True:
        try:
            entrada = input(mensaje).strip()
            assert entrada.replace(" ", "").isalpha()
            break
        except AssertionError:
            print("[ERROR] El nombre ingresado debe contener solo letras.")
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

def tipar_valor(entrada):
    texto = entrada.strip()

    try:
        return int(texto), "int"
    except ValueError:
        pass

    try: 
        return float(texto), "float"
    except ValueError:
        pass

    return texto, "str"


# ESTRUCTURAS INICIALES Y GENERACIÓN DE DATOS

def crear_agenda():
    return [
        {"id": 1, "nombre": "Juan Perez", "telefono": 123, "mail": "juan@gmail.com", "grupo": "Trabajo", "estado": "activo"},
        {"id": 2, "nombre": "Maria Gomez", "telefono": 1199887766, "mail": "maria@gmail.com", "grupo": "Familia", "estado": "activo"},
        {"id": 3, "nombre": "Lucas Silva", "telefono": 1144556677, "mail": "lucas@gmail.com", "grupo": "Amigos", "estado": "activo"}
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

def generar_muestra(datos, tipo):
    """
    Construye la línea de texto completa (base + campos extras) 
    para representar en pantalla un contacto o un grupo.
    """
    id_fmt = str(datos["id"]).zfill(4)

    if tipo == "contacto":
        linea_base = f"ID: {id_fmt:<5} | Nombre: {datos['nombre']:<18} | Tel: {datos['telefono']:<12} | Mail: {datos['mail']:<20} | Grupo: {datos['grupo']:<10}"
        campos_fijos = ["id", "nombre", "telefono", "mail", "grupo", "estado"]
    else:
        linea_base = f"ID: {id_fmt:<5} | Grupo: {datos['nombre']:<15} | Descripción: {datos['descripcion']:<35} | Prioridad: {datos['prioridad']:<10}"
        campos_fijos = ["id", "nombre", "descripcion", "prioridad"]

    campos_extras = {}
    for clave, valor in datos.items():
        if clave not in campos_fijos:
            campos_extras[clave] = valor

    if len(campos_extras) > 0:
        detalles = []
        for clave, valor in campos_extras.items():
            detalles.append(f"{clave}: {valor}")
        texto_extra = ", ".join(detalles)
        return f"{linea_base} | {texto_extra}"

    return linea_base

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

def obtener_contactos_activos(agenda):
    """Devuelve únicamente los contactos con estado activo."""
    return [c for c in agenda if c.get("estado", "activo") == "activo"]

def obtener_contactos_papelera(agenda):
    """Devuelve únicamente los contactos que están en la papelera."""
    return [c for c in agenda if c.get("estado") == "papelera"]

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
        "grupo": grupo,
        "estado": "activo"
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

def agregar_campo_personalizado(entidad, tipo_entidad):

    print(f"\n--- AGREGAR CAMPO EXTRA AL {tipo_entidad.upper()}: {entidad['nombre']} ---")

    clave = input("Ingrese el nombre del nuevo campo (ej: nota, edad, saldo): ").strip().lower()

    while clave in entidad or clave == "":
        if clave in entidad:
            print(f"[ERROR] El campo {clave} ya existe.")
        else:
            print(f"[ERROR] El nombre del campo no puede estar vacio.")
        
        clave = input("Ingrese el nombre del nuevo campo (ej: nota, edad, saldo): ").strip().lower()

    valor = input(f"Ingrese el valor del campo {clave}:  ").strip()
    while valor == "":
        print(f"[ERROR] El valor del campo no puede estar vacio.")
        valor = input(f"Ingres el valor del campo {clave}:  ").strip()

    valor_final, tipo_dato = tipar_valor(valor)
    entidad[clave] = valor_final

    print(f"[EXITO] Campo {clave} agregado con valor {valor_final} (Tipo: {tipo_dato})")

def eliminar_campo_personalizado(entidad, tipo_entidad):
    """
    Permite al usuario seleccionar y eliminar un campo extra existente.
    """
    if tipo_entidad == "contacto":
        campos_fijos = ["id", "nombre", "telefono", "mail", "grupo", "estado"]
    else:
        campos_fijos = ["id", "nombre", "descripcion", "prioridad"]

    claves_extras = []
    for clave in entidad.keys():
        if clave not in campos_fijos:
            claves_extras.append(clave)

    if len(claves_extras) == 0:
        print(f"\n[INFO] Este {tipo_entidad} no tiene campos extras para eliminar.")
        return

    opciones = []
    for clave in claves_extras:
        opciones.append(f"Eliminar '{clave}' (Valor actual: {entidad[clave]})")
    opciones.append("Cancelar")

    eleccion = menu_opciones(f"Eliminar Campo Extra de {entidad['nombre']}", opciones)

    if eleccion <= len(claves_extras):
        clave_a_borrar = claves_extras[eleccion - 1]
        entidad.pop(clave_a_borrar)
        print(f"[ÉXITO] El campo '{clave_a_borrar}' fue eliminado correctamente.")
    else:
        print("[INFO] Operación cancelada.")

def cambiar_dato(matriz, pos, nuevo_valor, clave):
    """Aplica la modificación in situ sobre la matriz de agenda."""
    matriz[pos][clave] = nuevo_valor
    print("[ÉXITO] Contacto modificado correctamente.")
    
def modificar_contacto(agenda, pos, grupos):
    """Muestra las opciones de modificar contacto y ejecuta el cambio"""
    opciones_modificar = ["Nombre", "Teléfono", "Mail", "Grupo", "Agregar Campo Extra", "Eliminar Campo Extra", "Cancelar"]
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
            agregar_campo_personalizado(agenda[pos], "contacto")
        case 6:
            eliminar_campo_personalizado(agenda[pos], "contacto")
        case 7:
            print("[INFO] Operación cancelada.")
            
def modificar_grupo(agenda, pos, grupos):
    opciones_modificar_grupo = ["Nombre del grupo", "Descripción", "Prioridad", "Agregar campo extra", "Eliminar Campo extra", "Cancelar"]
    eleccion = menu_opciones("Menú de Modificación de Grupo", opciones_modificar_grupo)
    match eleccion:
        case 1:
            nombre_anterior = grupos[pos]["nombre"]
            valor = validar_solo_letras("Dime el nuevo nombre: ")
            cambiar_dato(grupos, pos, valor.title(), "nombre")
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
            agregar_campo_personalizado(grupos[pos], "grupo")
        case 5:
            eliminar_campo_personalizado(grupos[pos], "grupo")
        case 6:
            print("[INFO] Operación cancelada.")

def gestionar_papelera(agenda):
    """Submenú para ver, restaurar o vaciar contactos eliminados."""
    ejecutando = True
    while ejecutando:
        papelera = obtener_contactos_papelera(agenda)
        print(f"\n=== PAPELERA DE RECICLAJE ({len(papelera)} contactos) ===")
        print("  [1] Ver contactos en la papelera")
        print("  [2] Restaurar un contacto")
        print("  [3] Vaciar la papelera (Eliminar todo definitivamente)")
        print("  [4] Eliminar un contacto de la papelera")
        print("  [5] Volver al menú principal")
        
        opcion = validar_numero("Seleccione una opción: ", 1, 5)
        
        match opcion:
            case 1:
                if not papelera:
                    print("\n[INFO] La papelera está vacía.")
                else:
                    for c in papelera:
                        mostrar_contacto(c)
            case 2:
                if not papelera:
                    print("\n[INFO] No hay contactos para restaurar.")
                else:
                    pos = buscar_por_id(agenda)
                    if pos != -1 and agenda[pos].get("estado") == "papelera":
                        agenda[pos]["estado"] = "activo"
                        print(f"[ÉXITO] Contacto '{agenda[pos]['nombre']}' restaurado correctamente.")
                    else:
                        print("[ERROR] El ID ingresado no corresponde a un contacto en la papelera.")
            case 3:
                if not papelera:
                    print("\n[INFO] La papelera ya está vacía.")
                else:
                    confirmacion = input("¿Está seguro de vaciar la papelera? Esta acción no se puede deshacer (S/N): ").strip().upper()
                    if confirmacion == "S":
                        for contacto in list(agenda):
                            if contacto.get("estado") == "papelera":
                                agenda.remove(contacto)
                    else:
                        print("[INFO] Operación cancelada.")
            case 4:
                if not papelera:
                    print("\n[INFO] No hay contactos para restaurar.")
                else:
                    pos = buscar_por_id(agenda)
                    if pos != -1 and agenda[pos].get("estado") == "papelera":
                        eliminado = agenda.pop(pos)
                        print(f"[ÉXITO] '{eliminado['nombre']}' fue eliminado permanentemente.")
                    else:
                        print("[ERROR] El ID ingresado no corresponde a un contacto en la papelera.")
            case 5:
                ejecutando = False


def eliminar_contacto(agenda):
    print("\n=== ELIMINAR CONTACTO ===")
    pos = buscar_por_id(agenda)
    
    if pos == -1 or agenda[pos].get("estado") == "papelera":
        print("[RESULTADO] Contacto no encontrado en la agenda activa.")
    else:
        contacto = agenda[pos]
        print(f"\nContacto seleccionado: {contacto['nombre']} (ID: {contacto['id']})")
        print("  [1] Mover a la papelera (recomendado)")
        print("  [2] Eliminar permanentemente")
        print("  [3] Cancelar")
        
        opcion = validar_numero("Seleccione una opción: ", 1, 3)
        
        match opcion:
            case 1:
                contacto["estado"] = "papelera"
                print(f"[ÉXITO] '{contacto['nombre']}' fue movido a la papelera.")
            case 2:
                eliminado = agenda.pop(pos)
                print(f"[ÉXITO] '{eliminado['nombre']}' fue eliminado permanentemente.")
            case 3:
                print("[INFO] Operación cancelada.")

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
    print(generar_muestra(contacto, "contacto"))

def mostrar_grupo(grupo):
    """Muestra la ficha detallada de un grupo accediendo por clave."""
    print(generar_muestra(grupo, "grupo"))
    
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
    activos = obtener_contactos_activos(agenda)
    agenda_ordenada = sorted(activos, key=lambda c: c["nombre"])
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
    activos = obtener_contactos_activos(agenda)
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
        "Gestionar Papelera de Reciclaje", # Opción agregada
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
                if pos == -1 or agenda[pos].get("estado") == "papelera":
                    print("[RESULTADO] Contacto activo no encontrado.")
                else:
                    modificar_contacto(agenda, pos, grupos)
            case 3:
                eliminar_contacto(agenda) 
            case 4:
                gestionar_papelera(agenda)
            case 5:
                eliminar_grupo(grupos, agenda)
            case 6:
                mostrar(agenda, grupos)
            case 7:
                eleccion_de_busqueda_contactos(agenda, grupos)
            case 8: 
                posGrupo = buscar_por_id(grupos)
                if posGrupo == -1:
                    print("[RESULTADO] Grupo no encontrado.")
                else:
                    modificar_grupo(agenda, posGrupo, grupos)
            case 9: 
                eleccion_de_busqueda_grupos(grupos)
            case 10:
                agregar_grupo(grupos)
            case 11:
                print("\n¡Gracias por usar la agenda! Saliendo...")
                ejecutando = False

main()