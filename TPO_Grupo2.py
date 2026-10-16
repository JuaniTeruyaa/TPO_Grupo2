import json

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
def leer_lista_json(ruta_archivo):
    """Convertie el archivo txt en formato JSON en una lista de diccionarios"""
    lista = []
    try:
        archivo = open(ruta_archivo, "rt", encoding="utf-8")
        for linea in archivo:
            linea_limpia = linea.strip()
            if linea_limpia:
                objeto = json.loads(linea_limpia)
                lista.append(objeto)
    except (FileNotFoundError, OSError):
        print("[ERROR] No se ha podida leer el archivo")
    except json.JSONDecodeError:
        print("[ERROR] Formato JSON inválido en alguna línea")
    finally:
        try:
            archivo.close()
        except NameError:
            pass
    return lista


def crear_agenda():
    """Crea la lista de diccionarios agenda"""
    return leer_lista_json("contactos.txt")        

def crear_grupos():
    """Retorna la matriz con la definición de los grupos y su nivel de prioridad."""
    return leer_lista_json("grupos.txt")  
            
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

def exportar_archivo(agenda, grupos):
        opciones = ["Exportar contacto(s)/grupo(s)", "Elegir datos especificos a exportar", "Salir"]
        eleccion = menu_opciones("Opciones", opciones)
        contacto_o_grupo=validar_numero("Elija entre contactos(1), Grupos(2)", 1, 2)
        match eleccion:
            case 1:
                if contacto_o_grupo==1:
                    ids=elegir_ids(agenda)
                    lista_contactos=guardar_diccionario_con_ids(agenda,ids)
                    crear_archivo(lista_contactos,"archivo_contactos.txt")
                else:
                    ids=elegir_ids(grupos)
                    lista_grupos=guardar_diccionario_con_ids(agenda,ids)
                    crear_archivo(lista_grupos,"archivo_grupos.txt")
            case 2:
                if contacto_o_grupo==1:
                    opciones=["id","nombre","telefono","mail","grupo","estado","salir"]
                    datos_elegidos=set()
                    dato=""
                    while dato!="salir":
                        dato=menu_opciones("Opciones",opciones)
                        dato=opciones[dato-1]
                        if dato!="salir":
                            datos_elegidos.add(dato)
                    list(datos_elegidos)
                    lista_contactos=guardar_diccionario_con_datos(agenda,datos_elegidos)
                    crear_archivo(lista_contactos,"archivo_datos_contactos.txt")
                else:
                    opciones=["id","nombre","descripcion","prioridad","salir"]
                    datos_elegidos=set()
                    dato=""
                    while dato!="salir":
                        dato=menu_opciones("Opciones",opciones)
                        dato=opciones[dato-1]
                        if dato!="salir":
                            datos_elegidos.add(dato)
                    list(datos_elegidos)
                    lista_grupos=guardar_diccionario_con_datos(grupos,datos_elegidos)
                    crear_archivo(lista_grupos,"archivo_datos_grupos.txt")
            case 3:
                return
        
def elegir_ids(matriz):
    ids=[]
    id_elementos=[elemento["id"] for elemento in matriz]
    while True:
        id_elegido=pedir_entero("Dime el id del que quieres exportar los datos, cuando quieras terminar ingresa un valor que ya ingresaste: ")
        if id_elegido in ids:
            break
        elif id_elegido in id_elementos:
            ids.append(id_elegido)
        else:
            print("Ese id no esta")
    return ids

def guardar_diccionario_con_ids(matriz,ids):
    lista_diccionarios=[]
    for elemento in matriz:
        if elemento["id"] in ids:
            lista_diccionarios.append(elemento)
    return lista_diccionarios

def guardar_diccionario_con_datos(lista,datos_elegidos):
    lista_diccionarios = []

    for elemento in lista:
        nuevo_diccionario = {}
        for clave in datos_elegidos:
            if clave in elemento:
                nuevo_diccionario[clave] = elemento[clave]
        lista_diccionarios.append(nuevo_diccionario)
    return lista_diccionarios
        
            
def crear_archivo(lista,nombre_archivo):
    try:
        archivo = open(nombre_archivo,"wt",encoding="utf-8")
        for elemento in lista:
            dato=json.dumps(elemento,ensure_ascii=False)
            archivo.write(dato + "\n")
    except TypeError:
        print("[ERROR] Un elemento de la lista no se puede convertir a JSON.")
    finally:
        if archivo is not None:
            archivo.close()
        
def leer_archivo_externo():
    nombre=input("Dime el nombre del archivo a leer sin la extension de formato (ejemplo .txt),\ndebe estar en la carpeta del programa:")
    nombre+=".txt"
    print(nombre)
    return leer_lista_json(nombre)
            
# VISUALIZACIÓN

def mostrar_contacto(contacto):
    """Muestra la ficha detallada de un contacto accediendo por clave."""
    print(generar_muestra(contacto, "contacto"))

def mostrar_grupo(grupo):
    """Muestra la ficha detallada de un grupo accediendo por clave."""
    print(generar_muestra(grupo, "grupo"))
    
def mostrar_matriz_formateada(titulo, datos, cabeceras):
    """Imprime cualquier matriz en formato tabla asegurando ancho uniforme con rebanadas."""
    linea_cabecera = " | ".join([f"{h:^15}" for h in cabeceras])
    print(f"\n{titulo.upper().center(len(linea_cabecera),'-')}")
    print("=" * len(linea_cabecera))
    print(linea_cabecera)
    print("=" * len(linea_cabecera))
    
    for fila in datos:
        fila_str = [str(elem)[:15] for elem in fila]
        fila_str[0] = fila_str[0].zfill(4)
        print(" | ".join([f"{col:<15}" for col in fila_str]))
    print("=" * len(linea_cabecera))
    
def mostrar_matriz_distinta(datos,titulo="Datos"):
    """Muestra una lista de diccionarios en formato tabular.

    Detecta las claves del primer elemento para crear los títulos.
    """
    """Convierte la lista de diccionarios a matriz y llama a mostrar_matriz_formateada."""
    if not datos:
        print(f"[AVISO] No hay datos para mostrar en {titulo}")
        return
    else:
        cabeceras = list(datos[0].keys())
        matriz_datos = []
        for dicc in datos:
            fila = [dicc.get(clave, "") for clave in cabeceras]
            matriz_datos.append(fila)
        mostrar_matriz_formateada(titulo, matriz_datos, cabeceras)

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
        "Exportar un archivo",
        "Leer un archivo externo",
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
                exportar_archivo(agenda, grupos)
            case 12:
                datos=leer_archivo_externo()
                mostrar_matriz_distinta(datos)
            case 13:
                print("\n¡Gracias por usar la agenda! Saliendo...")
                ejecutando = False

main()