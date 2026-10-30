import json
import os

# ==========================================
# FUNCIONES AUXILIARES Y VALIDACIONES
# ==========================================

def pedir_entero(mensaje):
    """Solicita al usuario una entrada y valida que sea un número entero positivo mediante excepciones."""
    while True:
        try:
            entrada = input(mensaje).strip()
            num = int(entrada)
            if num <= 0:
                raise ValueError("El número debe ser mayor a 0.")
            return num
        except ValueError:
            print("[ERROR] Entrada inválida. Ingrese un número entero positivo.")

def validar_numero(mensaje, inicio, final):
    """Valida que un número ingresado por teclado esté dentro de un rango determinado."""
    while True:
        numero = pedir_entero(mensaje)
        if inicio <= numero <= final:
            return numero
        print(f"[ERROR] El número debe estar entre {inicio} y {final}.")

def convertidor_texto(texto):
    """Limpia un texto removiendo espacios en los extremos y convirtiéndolo a minúsculas."""
    return str(texto).strip().replace(" ", "").lower()

def validar_solo_letras(mensaje):
    """Pide un texto por teclado y asegura que contenga solo caracteres alfabéticos usando excepciones."""
    while True:
        try:
            entrada = input(mensaje).strip()
            if not entrada.replace(" ", "").isalpha() or len(entrada) == 0:
                raise ValueError("Debe contener únicamente letras.")
            return entrada.title()
        except ValueError as e:
            print(f"[ERROR] {e}")

def validar_formato_mail(mail):
    """Verifica si el mail contiene la estructura válida: texto@texto.texto"""
    partes = mail.split("@")
    if len(partes) != 2:
        return False
    if partes[0] == "" or partes[1] == "":
        return False
    if "." not in partes[1]:
        return False
        
    partes_dominio = partes[1].split(".")
    for parte in partes_dominio:
        if parte == "":
            return False
    return True

def tipar_valor(entrada):
    """Tipa automáticamente una entrada a int, float o str usando excepciones."""
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

def menu_opciones(titulo, opciones):
    """Muestra un menú enumerado dinámicamente y retorna la selección del usuario."""
    print(f"\n=== {titulo.upper()} ===")
    for i in range(len(opciones)):
        print(f"  [{i + 1}] {opciones[i]}")
    return validar_numero(f"Seleccione una opción (1-{len(opciones)}): ", 1, len(opciones))

def generar_muestra(datos, tipo_registro):
    """
    Construye la línea de texto formateada para representar
    en pantalla un contacto o un grupo individual.
    """
    id_fmt = str(datos.get("id", 0)).zfill(4)

    if tipo_registro == "contacto":
        linea_base = f"ID: {id_fmt:<5} | Nombre: {datos.get('nombre', ''):<18} | Tel: {datos.get('telefono', ''):<12} | Mail: {datos.get('mail', ''):<20} | Grupo: {datos.get('grupo', ''):<10}"
        campos_fijos = ("id", "nombre", "telefono", "mail", "grupo", "estado")
    else:
        linea_base = f"ID: {id_fmt:<5} | Grupo: {datos.get('nombre', ''):<15} | Descripción: {datos.get('descripcion', ''):<35} | Prioridad: {datos.get('prioridad', ''):<10}"
        campos_fijos = ("id", "nombre", "descripcion", "prioridad")

    campos_extras = {}
    for clave, valor in datos.items():
        if clave not in campos_fijos:
            campos_extras[clave] = valor

    if len(campos_extras) > 0:
        detalles = [f"{clave}: {valor}" for clave, valor in campos_extras.items()]
        texto_extra = ", ".join(detalles)
        return f"{linea_base} | {texto_extra}"

    return linea_base

def mostrar_contacto(contacto):
    """Muestra la ficha de un contacto."""
    print(generar_muestra(contacto, "contacto"))

def mostrar_grupo(grupo):
    """Muestra la ficha de un grupo."""
    print(generar_muestra(grupo, "grupo"))

# ==========================================
# MANEJO DE ARCHIVOS SECUENCIAL
# ==========================================

def sobrescribir_archivo(ruta_temp, ruta_destino):
    """
    Borra el archivo original y renombra el archivo temporal 
    para que pase a ser el definitivo usando el módulo 'os'.
    """
    try:
        # os.replace mueve/renombra el archivo temporal a la ruta destino.
        # Si el archivo destino ya existe, lo borra y lo pisa automáticamente.
        os.replace(ruta_temp, ruta_destino)
    except OSError as e:
        print(f"[ERROR] Ocurrió un error al reemplazar el archivo: {e}")

def generar_id_unico_archivo(ruta_archivo):
    """
    Determina el ID máximo leyendo el archivo secuencialmente línea por línea.
    """
    max_id = 0
    try:
        arch = open(ruta_archivo, "rt", encoding="utf-8")
        for linea in arch:
            linea_limpia = linea.strip()
            if linea_limpia:
                objeto = json.loads(linea_limpia)
                if objeto.get("id", 0) > max_id:
                    max_id = objeto["id"]
    except FileNotFoundError:
        pass
    except OSError as error:
        print(f"[ERROR] Error al determinar el ID único: {error}")
    finally:
        try:
            arch.close()
        except NameError:
            pass
    return max_id + 1

def obtener_grupos_lista(ruta_archivo="grupos.txt"):
    """
    Lee secuencialmente los grupos para devolver únicamente una lista con los nombres.
    (Sólo retiene los nombres como string para poder renderizar las opciones del menú)
    """
    grupos_nombres = []
    try:
        arch = open(ruta_archivo, "rt", encoding="utf-8")
        for linea in arch:
            linea_limpia = linea.strip()
            if linea_limpia:
                g = json.loads(linea_limpia)
                grupos_nombres.append(g["nombre"])
    except FileNotFoundError:
        print("[AVISO] El archivo de grupos no existe aún.")
    except OSError as error:
        print(f"[ERROR] No se pudieron leer los grupos: {error}")
    finally:
        try:
            arch.close()
        except NameError:
            pass
    return grupos_nombres

def seleccionar_grupo_desde_archivo(ruta_archivo="grupos.txt"):
    """Permite al usuario seleccionar un grupo leyendo las opciones desde el archivo."""
    grupos = obtener_grupos_lista(ruta_archivo)
    if not grupos:
        print("[AVISO] No hay grupos registrados. Se asignará el grupo 'Varios'.")
        return "Varios"
    
    eleccion = menu_opciones("Seleccionar Grupo", grupos)
    return grupos[eleccion - 1]

def buscar_por_id_archivo(id_buscado, ruta_archivo):
    """
    Busca un objeto por su ID recorriendo el archivo línea por línea.
    No carga todos los datos, se detiene al encontrarlo.
    """
    encontrado = None
    try:
        arch = open(ruta_archivo, "rt", encoding="utf-8")
        for linea in arch:
            linea_limpia = linea.strip()
            if linea_limpia:
                objeto = json.loads(linea_limpia)
                if objeto.get("id") == id_buscado:
                    encontrado = objeto
                    break
    except FileNotFoundError:
        print(f"[ERROR] El archivo '{ruta_archivo}' no existe.")
    except OSError as error:
        print(f"[ERROR] Error al leer el archivo: {error}")
    finally:
        try:
            arch.close()
        except NameError:
            pass
    return encontrado


# ==========================================
# CONSULTAS Y BÚSQUEDAS (MODO CONSULTA)
# ==========================================

def consultar_por_filtro(clave_filtro, valor_buscado, tipo_busqueda, ruta_archivo):
    """Recorre el archivo línea por línea buscando coincidencias."""
    cantidad = 0
    valor_limpio = convertidor_texto(valor_buscado)

    try:
        arch = open(ruta_archivo, "rt", encoding="utf-8")
        print(f"\n--- RESULTADOS DE BÚSQUEDA ---")
        for linea in arch:
            linea_limpia = linea.strip()
            if linea_limpia:
                registro = json.loads(linea_limpia)
                
                if registro.get("estado") == "papelera":
                    continue
                    
                campo_valor = registro.get(clave_filtro, "")
                campo_str = convertidor_texto(campo_valor)

                coincide = False
                if tipo_busqueda == "igual":
                    coincide = (campo_str == valor_limpio)
                elif tipo_busqueda == "subcadena":
                    coincide = (valor_limpio in campo_str)

                if coincide:
                    if "prioridad" in registro:
                        mostrar_grupo(registro)
                    else:
                        mostrar_contacto(registro)
                    cantidad += 1

        if cantidad == 0:
            print("[RESULTADO] No se encontraron resultados con ese criterio.")
        else:
            print(f"[INFO] Total encontrados: {cantidad}")

    except FileNotFoundError:
        print(f"[ERROR] No se encontró el archivo '{ruta_archivo}'.")
    except OSError as error:
        print(f"[ERROR] Error al leer el archivo: {error}")
    finally:
        try:
            arch.close()
        except NameError:
            pass


# ==========================================
# OPERACIONES DE ESCRITURA (ALTAS, BAJAS, MODIFICACIONES)
# ==========================================

def agregar_contacto_archivo(ruta_contactos="contactos.txt", ruta_grupos="grupos.txt"):
    """Registra un nuevo contacto agregando una línea JSON al final del archivo."""
    print("\n=== AGREGAR NUEVO CONTACTO ===")
    nuevo_id = generar_id_unico_archivo(ruta_contactos)
    nombre = validar_solo_letras("Ingrese el nombre completo: ")
    telefono = pedir_entero("Ingrese el número de teléfono: ")
    mail = input("Ingrese el correo electrónico: ").strip().lower()
    while not validar_formato_mail(mail):
        print("[ERROR] El correo no tiene un formato válido (ejemplo: usuario@dominio.com).")
        mail = input("Ingrese otro correo electrónico: ").strip().lower()
    grupo = seleccionar_grupo_desde_archivo(ruta_grupos)

    nuevo_contacto = {
        "id": nuevo_id,
        "nombre": nombre,
        "telefono": telefono,
        "mail": mail,
        "grupo": grupo,
        "estado": "activo"
    }

    try:
        arch = open(ruta_contactos, "at", encoding="utf-8")
        arch.write(json.dumps(nuevo_contacto, ensure_ascii=False) + "\n")
        print(f"\n[ÉXITO] Contacto '{nombre}' agregado con éxito (ID asignado: {nuevo_id}).")
    except OSError as error:
        print(f"[ERROR] No se pudo guardar el contacto: {error}")
    finally:
        try:
            arch.close()
        except NameError:
            pass

def agregar_grupo_archivo(ruta_grupos="grupos.txt"):
    """Registra un nuevo grupo agregando una línea JSON al archivo de grupos."""
    print("\n=== AGREGAR NUEVO GRUPO ===")
    nuevo_id = generar_id_unico_archivo(ruta_grupos)
    nombre = validar_solo_letras("Ingrese el nombre del grupo: ")
    descripcion = input("Ingrese la descripción del grupo: ").strip()
    opciones_prioridades = ("Alta", "Media", "Baja")
    eleccion_prio = menu_opciones("Prioridad", opciones_prioridades)
    prioridad = opciones_prioridades[eleccion_prio - 1]

    nuevo_grupo = {
        "id": nuevo_id,
        "nombre": nombre,
        "descripcion": descripcion,
        "prioridad": prioridad
    }

    try:
        arch = open(ruta_grupos, "at", encoding="utf-8")
        arch.write(json.dumps(nuevo_grupo, ensure_ascii=False) + "\n")
        print(f"\n[ÉXITO] Grupo '{nombre}' agregado con éxito (ID asignado: {nuevo_id}).")
    except OSError as error:
        print(f"[ERROR] No se pudo guardar el grupo: {error}")
    finally:
        try:
            arch.close()
        except NameError:
            pass

def agregar_campo_personalizado(registro, tipo_seccion):
    """Agrega una clave-valor extra al diccionario de un contacto o grupo."""
    print(f"\n--- AGREGAR CAMPO EXTRA EN {tipo_seccion.upper()}: {registro['nombre']} ---")
    clave = input("Ingrese el nombre del nuevo campo (ej: nota, edad, saldo): ").strip().lower()

    while clave in registro or clave == "":
        if clave in registro:
            print(f"[ERROR] El campo '{clave}' ya existe.")
        else:
            print("[ERROR] El nombre del campo no puede estar vacío.")
        clave = input("Ingrese el nombre del nuevo campo: ").strip().lower()

    valor = input(f"Ingrese el valor del campo '{clave}': ").strip()
    while valor == "":
        print("[ERROR] El valor del campo no puede estar vacío.")
        valor = input(f"Ingrese el valor del campo '{clave}': ").strip()

    valor_final, tipo_dato = tipar_valor(valor)
    registro[clave] = valor_final
    print(f"[ÉXITO] Campo '{clave}' agregado con valor '{valor_final}' (Tipo: {tipo_dato}).")

def eliminar_campo_personalizado(registro, tipo_seccion):
    """Permite seleccionar y eliminar un campo personalizado extra existente."""
    if tipo_seccion == "contacto":
        campos_fijos = ("id", "nombre", "telefono", "mail", "grupo", "estado")
    else:
        campos_fijos = ("id", "nombre", "descripcion", "prioridad")

    claves_extras = [clave for clave in registro.keys() if clave not in campos_fijos]

    if not claves_extras:
        print(f"\n[INFO] Este registro de {tipo_seccion} no tiene campos extras para eliminar.")
        return

    opciones = [f"Eliminar '{clave}' (Valor actual: {registro[clave]})" for clave in claves_extras]
    opciones.append("Cancelar")

    eleccion = menu_opciones(f"Eliminar Campo Extra de {registro['nombre']}", opciones)

    if eleccion <= len(claves_extras):
        clave_a_borrar = claves_extras[eleccion - 1]
        registro.pop(clave_a_borrar)
        print(f"[ÉXITO] El campo '{clave_a_borrar}' fue eliminado correctamente.")
    else:
        print("[INFO] Operación cancelada.")

def modificar_contacto_archivo(ruta_contactos="contactos.txt", ruta_grupos="grupos.txt"):
    """
    Busca un contacto por ID, aplica las modificaciones y sobrescribe el archivo secuencialmente.
    """
    print("\n=== MODIFICAR CONTACTO ===")
    id_buscado = pedir_entero("Dime el ID del contacto a modificar: ")
    
    contacto_objetivo = buscar_por_id_archivo(id_buscado, ruta_contactos)
    if not contacto_objetivo or contacto_objetivo.get("estado") == "papelera":
        print("[RESULTADO] Contacto activo no encontrado.")
        return

    print("\nContacto seleccionado:")
    mostrar_contacto(contacto_objetivo)

    opciones_modificar = [
        "Nombre", "Teléfono", "Mail", "Grupo", 
        "Agregar Campo Extra", "Eliminar Campo Extra", "Cancelar"
    ]
    eleccion = menu_opciones("Menú de Modificación", opciones_modificar)

    modificado = True
    match eleccion:
        case 1:
            contacto_objetivo["nombre"] = validar_solo_letras("Dime el nuevo nombre: ")
        case 2:
            contacto_objetivo["telefono"] = pedir_entero("Dime el nuevo teléfono: ")
        case 3:
            valor = input("Dime el nuevo mail: ").strip().lower()
            while not validar_formato_mail(valor):
                print("[ERROR] El correo no es válido.")
                valor = input("Dime el nuevo mail: ").strip().lower()
            contacto_objetivo["mail"] = valor
        case 4:
            contacto_objetivo["grupo"] = seleccionar_grupo_desde_archivo(ruta_grupos)
        case 5:
            agregar_campo_personalizado(contacto_objetivo, "contacto")
        case 6:
            eliminar_campo_personalizado(contacto_objetivo, "contacto")
        case 7:
            print("[INFO] Operación cancelada.")
            modificado = False

    if not modificado:
        return

    ruta_temp = "temp_contactos.txt"

    try:
        arch_orig = open(ruta_contactos, "rt", encoding="utf-8")
        arch_temp = open(ruta_temp, "wt", encoding="utf-8")

        for linea in arch_orig:
            linea_limpia = linea.strip()
            if linea_limpia:
                c = json.loads(linea_limpia)
                if c.get("id") == id_buscado:
                    arch_temp.write(json.dumps(contacto_objetivo, ensure_ascii=False) + "\n")
                else:
                    arch_temp.write(linea)

        print("[ÉXITO] Contacto modificado correctamente.")

    except OSError as error:
        print(f"[ERROR] Ocurrió un error al actualizar el archivo: {error}")
    finally:
        try:
            arch_orig.close()
        except NameError:
            pass
        try:
            arch_temp.close()
        except NameError:
            pass

    sobrescribir_archivo(ruta_temp, ruta_contactos)

def reasignar_contactos_de_grupo(nombre_grupo_viejo, nombre_grupo_nuevo, ruta_contactos="contactos.txt"):
    """
    Recorre el archivo de contactos para reasignar cualquier contacto perteneciente 
    a un grupo hacia uno nuevo.
    """
    ruta_temp = "temp_contactos_reasignar.txt"
    v_limpio = convertidor_texto(nombre_grupo_viejo)

    try:
        arch_orig = open(ruta_contactos, "rt", encoding="utf-8")
        arch_temp = open(ruta_temp, "wt", encoding="utf-8")

        for linea in arch_orig:
            linea_limpia = linea.strip()
            if linea_limpia:
                contacto = json.loads(linea_limpia)
                if convertidor_texto(contacto.get("grupo", "")) == v_limpio:
                    contacto["grupo"] = nombre_grupo_nuevo
                arch_temp.write(json.dumps(contacto, ensure_ascii=False) + "\n")

    except OSError as error:
        print(f"[ERROR] Error al reasignar contactos de grupo: {error}")
    finally:
        try:
            arch_orig.close()
        except NameError:
            pass
        try:
            arch_temp.close()
        except NameError:
            pass

    sobrescribir_archivo(ruta_temp, ruta_contactos)

def modificar_grupo_archivo(ruta_grupos="grupos.txt", ruta_contactos="contactos.txt"):
    """Modifica los atributos de un grupo y sobrescribe el archivo."""
    print("\n=== MODIFICAR GRUPO ===")
    id_buscado = pedir_entero("Dime el ID del grupo a modificar: ")

    grupo_objetivo = buscar_por_id_archivo(id_buscado, ruta_grupos)
    if not grupo_objetivo:
        print("[RESULTADO] Grupo no encontrado.")
        return

    print("\nGrupo seleccionado:")
    mostrar_grupo(grupo_objetivo)

    opciones_modificar_grupo = [
        "Nombre del grupo", "Descripción", "Prioridad", 
        "Agregar campo extra", "Eliminar campo extra", "Cancelar"
    ]
    eleccion = menu_opciones("Menú de Modificación de Grupo", opciones_modificar_grupo)

    nombre_anterior = grupo_objetivo["nombre"]
    modificado = True
    renombrado = False

    match eleccion:
        case 1:
            nuevo_nombre = validar_solo_letras("Dime el nuevo nombre: ")
            grupo_objetivo["nombre"] = nuevo_nombre
            renombrado = True
        case 2:
            grupo_objetivo["descripcion"] = input("Dime la nueva descripción del grupo: ").strip()
        case 3:
            prioridades = ("Alta", "Media", "Baja")
            eleccion_prio = menu_opciones("Prioridad", prioridades)
            grupo_objetivo["prioridad"] = prioridades[eleccion_prio - 1]
        case 4:
            agregar_campo_personalizado(grupo_objetivo, "grupo")
        case 5:
            eliminar_campo_personalizado(grupo_objetivo, "grupo")
        case 6:
            print("[INFO] Operación cancelada.")
            modificado = False

    if not modificado:
        return

    ruta_temp = "temp_grupos.txt"

    try:
        arch_orig = open(ruta_grupos, "rt", encoding="utf-8")
        arch_temp = open(ruta_temp, "wt", encoding="utf-8")

        for linea in arch_orig:
            linea_limpia = linea.strip()
            if linea_limpia:
                g = json.loads(linea_limpia)
                if g.get("id") == id_buscado:
                    arch_temp.write(json.dumps(grupo_objetivo, ensure_ascii=False) + "\n")
                else:
                    arch_temp.write(linea)

        print("[ÉXITO] Grupo modificado correctamente.")

    except OSError as error:
        print(f"[ERROR] Error al modificar grupo: {error}")
    finally:
        try:
            arch_orig.close()
        except NameError:
            pass
        try:
            arch_temp.close()
        except NameError:
            pass

    sobrescribir_archivo(ruta_temp, ruta_grupos)

    if renombrado:
        reasignar_contactos_de_grupo(nombre_anterior, grupo_objetivo["nombre"], ruta_contactos)

def eliminar_contacto_archivo(ruta_contactos="contactos.txt", ruta_papelera="papelera_contactos.txt"):
    """
    Elimina un contacto. Puede moverlo físicamente al archivo de la papelera
    o eliminarlo definitivamente del archivo principal.
    """
    print("\n=== ELIMINAR CONTACTO ===")
    id_buscado = pedir_entero("Dime el ID del contacto a eliminar: ")

    contacto_objetivo = buscar_por_id_archivo(id_buscado, ruta_contactos)
    if not contacto_objetivo or contacto_objetivo.get("estado") == "papelera":
        print("[RESULTADO] Contacto activo no encontrado.")
        return

    print(f"\nContacto seleccionado: {contacto_objetivo['nombre']} (ID: {contacto_objetivo['id']})")
    print("  [1] Mover a la papelera (Recomendado)")
    print("  [2] Eliminar permanentemente")
    print("  [3] Cancelar")

    opcion = validar_numero("Seleccione una opción: ", 1, 3)
    if opcion == 3:
        print("[INFO] Operación cancelada.")
        return

    ruta_temp = "temp_contactos.txt"

    try:
        arch_orig = open(ruta_contactos, "rt", encoding="utf-8")
        arch_temp = open(ruta_temp, "wt", encoding="utf-8")

        if opcion == 1:
            arch_papelera = open(ruta_papelera, "at", encoding="utf-8")

        for linea in arch_orig:
            linea_limpia = linea.strip()
            if linea_limpia:
                c = json.loads(linea_limpia)
                if c.get("id") == id_buscado:
                    if opcion == 1:
                        c["estado"] = "papelera"
                        arch_papelera.write(json.dumps(c, ensure_ascii=False) + "\n")
                        print(f"[ÉXITO] '{c['nombre']}' fue movido a la papelera.")
                    else:
                        print(f"[ÉXITO] '{c['nombre']}' fue eliminado permanentemente.")
                else:
                    arch_temp.write(linea)

    except OSError as error:
        print(f"[ERROR] Error durante la eliminación: {error}")
    finally:
        try:
            arch_orig.close()
        except NameError:
            pass
        try:
            arch_temp.close()
        except NameError:
            pass
        try:
            arch_papelera.close()
        except NameError:
            pass

    sobrescribir_archivo(ruta_temp, ruta_contactos)

def eliminar_grupo_archivo(ruta_grupos="grupos.txt", ruta_contactos="contactos.txt"):
    """Elimina un grupo reasignando sus contactos en el archivo de contactos hacia 'Varios'."""
    print("\n=== ELIMINAR GRUPO ===")
    id_buscado = pedir_entero("Dime el ID del grupo a eliminar: ")

    grupo_objetivo = buscar_por_id_archivo(id_buscado, ruta_grupos)
    if not grupo_objetivo:
        print("[RESULTADO] Grupo no encontrado.")
        return

    nombre_grupo = grupo_objetivo["nombre"]
    if convertidor_texto(nombre_grupo) == "varios":
        print("[ERROR] No se puede eliminar el grupo por defecto 'Varios'.")
        return

    ruta_temp = "temp_grupos.txt"

    try:
        arch_orig = open(ruta_grupos, "rt", encoding="utf-8")
        arch_temp = open(ruta_temp, "wt", encoding="utf-8")

        for linea in arch_orig:
            linea_limpia = linea.strip()
            if linea_limpia:
                g = json.loads(linea_limpia)
                if g.get("id") == id_buscado:
                    print(f"[ÉXITO] Grupo '{nombre_grupo}' eliminado.")
                else:
                    arch_temp.write(linea)

    except OSError as error:
        print(f"[ERROR] Error al eliminar el grupo: {error}")
    finally:
        try:
            arch_orig.close()
        except NameError:
            pass
        try:
            arch_temp.close()
        except NameError:
            pass

    sobrescribir_archivo(ruta_temp, ruta_grupos)
    reasignar_contactos_de_grupo(nombre_grupo, "Varios", ruta_contactos)


# ==========================================
# GESTIÓN DE LA PAPELERA DE RECICLAJE
# ==========================================

def gestionar_papelera_archivo(ruta_contactos="contactos.txt", ruta_papelera="papelera_contactos.txt"):
    """Submenú interactivo para gestionar la papelera de reciclaje."""
    ejecutando = True
    while ejecutando:
        print("\n=== PAPELERA DE RECICLAJE ===")
        print("  [1] Ver contactos en la papelera")
        print("  [2] Restaurar un contacto")
        print("  [3] Vaciar la papelera (Eliminar todo definitivamente)")
        print("  [4] Eliminar un contacto permanentemente de la papelera")
        print("  [5] Volver al menú anterior")

        opcion = validar_numero("Seleccione una opción: ", 1, 5)

        match opcion:
            case 1:
                cant = 0
                try:
                    arch = open(ruta_papelera, "rt", encoding="utf-8")
                    print("\n--- CONTACTOS EN LA PAPELERA ---")
                    for linea in arch:
                        linea_limpia = linea.strip()
                        if linea_limpia:
                            contacto = json.loads(linea_limpia)
                            mostrar_contacto(contacto)
                            cant += 1
                    if cant == 0:
                        print("[INFO] La papelera está vacía.")
                except FileNotFoundError:
                    print("[INFO] La papelera está vacía (no existe archivo de papelera).")
                except OSError as error:
                    print(f"[ERROR] Error al leer la papelera: {error}")
                finally:
                    try:
                        arch.close()
                    except NameError:
                        pass

            case 2:
                id_buscado = pedir_entero("Dime el ID del contacto a restaurar: ")
                contacto_papelera = buscar_por_id_archivo(id_buscado, ruta_papelera)

                if not contacto_papelera:
                    print("[ERROR] El ID ingresado no corresponde a un contacto en la papelera.")
                    continue

                ruta_temp = "temp_papelera.txt"

                try:
                    arch_pap = open(ruta_papelera, "rt", encoding="utf-8")
                    arch_temp = open(ruta_temp, "wt", encoding="utf-8")
                    arch_cont = open(ruta_contactos, "at", encoding="utf-8")

                    for linea in arch_pap:
                        linea_limpia = linea.strip()
                        if linea_limpia:
                            c = json.loads(linea_limpia)
                            if c.get("id") == id_buscado:
                                c["estado"] = "activo"
                                arch_cont.write(json.dumps(c, ensure_ascii=False) + "\n")
                                print(f"[ÉXITO] Contacto '{c['nombre']}' restaurado a la agenda activa.")
                            else:
                                arch_temp.write(linea)

                except OSError as error:
                    print(f"[ERROR] Error durante la restauración: {error}")
                finally:
                    try:
                        arch_pap.close()
                    except NameError:
                        pass
                    try:
                        arch_temp.close()
                    except NameError:
                        pass
                    try:
                        arch_cont.close()
                    except NameError:
                        pass

                sobrescribir_archivo(ruta_temp, ruta_papelera)

            case 3:
                confirmacion = input("¿Está seguro de vaciar la papelera? (S/N): ").strip().upper()
                if confirmacion == "S":
                    try:
                        arch = open(ruta_papelera, "wt", encoding="utf-8")
                        arch.close()
                        print("[ÉXITO] La papelera se ha vaciado por completo.")
                    except OSError as error:
                        print(f"[ERROR] No se pudo vaciar la papelera: {error}")
                else:
                    print("[INFO] Operación cancelada.")

            case 4:
                id_buscado = pedir_entero("Dime el ID del contacto a borrar permanentemente: ")
                contacto_papelera = buscar_por_id_archivo(id_buscado, ruta_papelera)

                if not contacto_papelera:
                    print("[ERROR] El ID ingresado no corresponde a un contacto en la papelera.")
                    continue

                ruta_temp = "temp_papelera.txt"

                try:
                    arch_pap = open(ruta_papelera, "rt", encoding="utf-8")
                    arch_temp = open(ruta_temp, "wt", encoding="utf-8")

                    for linea in arch_pap:
                        linea_limpia = linea.strip()
                        if linea_limpia:
                            c = json.loads(linea_limpia)
                            if c.get("id") == id_buscado:
                                print(f"[ÉXITO] '{c['nombre']}' fue eliminado permanentemente de la papelera.")
                            else:
                                arch_temp.write(linea)

                except OSError as error:
                    print(f"[ERROR] Error al eliminar de la papelera: {error}")
                finally:
                    try:
                        arch_pap.close()
                    except NameError:
                        pass
                    try:
                        arch_temp.close()
                    except NameError:
                        pass

                sobrescribir_archivo(ruta_temp, ruta_papelera)

            case 5:
                ejecutando = False


# ==========================================
# EXPORTAR Y LEER ARCHIVOS EXTERNOS
# ==========================================

def exportar_archivo_secuencial(ruta_contactos="contactos.txt", ruta_grupos="grupos.txt"):
    """
    Exporta datos iterando el archivo secuencialmente. 
    Aplica un doble filtro: primero por IDs específicos y luego por los campos deseados.
    """
    print("\n=== EXPORTACIÓN DE DATOS ===")
    opciones_seccion = ["Contactos", "Grupos", "Cancelar"]
    eleccion_seccion = menu_opciones("Elija sección a exportar", opciones_seccion)
    
    if eleccion_seccion == 3:
        print("[INFO] Exportación cancelada.")
        return

    ruta_origen = ruta_contactos if eleccion_seccion == 1 else ruta_grupos
    nombre_salida = "export_contactos.txt" if eleccion_seccion == 1 else "export_grupos.txt"

    # 1. FILTRO DE REGISTROS (Por ID)
    print("\n--- 1. INGRESAR IDs A EXPORTAR ---")
    ids_deseados = set()
    while True:
        id_ingresado = pedir_entero("Ingrese ID a exportar (o vuelva a ingresar un ID ya añadido para finalizar): ")
        if id_ingresado in ids_deseados:
            break
        ids_deseados.add(id_ingresado)
        
    if not ids_deseados:
        print("[INFO] No se seleccionó ningún ID. Cancelando exportación.")
        return

    # 2. FILTRO DE DATOS (Por campos)
    print("\n--- 2. SELECCIÓN DE CAMPOS A EXPORTAR ---")
    opciones_tipo_exportacion = [
        "Exportar TODOS los campos (incluye campos extra personalizados)", 
        "Seleccionar campos específicos manualmente"
    ]
    eleccion_campos = menu_opciones("Tipo de exportación", opciones_tipo_exportacion)
    
    campos_elegidos = set()
    campos_disponibles = (
        ["id", "nombre", "telefono", "mail", "grupo", "estado"] 
        if eleccion_seccion == 1 else ["id", "nombre", "descripcion", "prioridad"]
    )

    if eleccion_campos == 2:
        opciones_menu = campos_disponibles + ["Finalizar selección"]
        while True:
            sel = menu_opciones("Campos Disponibles", opciones_menu)
            if sel == len(opciones_menu):
                break
            campo = opciones_menu[sel - 1]
            campos_elegidos.add(campo)
            print(f"[INFO] Campos seleccionados actual: {list(campos_elegidos)}")

        if not campos_elegidos:
            print("[INFO] No se seleccionó ningún campo. Cancelando exportación.")
            return

    # 3. EJECUCIÓN DE EXPORTACIÓN (Una sola lectura)
    cant = 0

    try:
        arch_orig = open(ruta_origen, "rt", encoding="utf-8")
        arch_dest = open(nombre_salida, "wt", encoding="utf-8")

        for linea in arch_orig:
            linea_limpia = linea.strip()
            if linea_limpia:
                objeto = json.loads(linea_limpia)
                
                if objeto.get("id") in ids_deseados:
                    
                    if eleccion_campos == 1:
                        arch_dest.write(json.dumps(objeto, ensure_ascii=False) + "\n")
                    else:
                        nuevo_dict = {k: objeto[k] for k in campos_elegidos if k in objeto}
                        arch_dest.write(json.dumps(nuevo_dict, ensure_ascii=False) + "\n")
                    
                    cant += 1

        print(f"[ÉXITO] Se exportaron {cant} registros con éxito al archivo '{nombre_salida}'.")

    except FileNotFoundError:
        print(f"[ERROR] El archivo de origen '{ruta_origen}' no existe.")
    except OSError as error:
        print(f"[ERROR] Error durante la exportación: {error}")
    finally:
        try:
            arch_orig.close()
        except NameError:
            pass
        try:
            arch_dest.close()
        except NameError:
            pass

def leer_archivo_externo():
    """Lee secuencialmente e imprime por pantalla el contenido de un archivo externo."""
    nombre = input("Ingrese el nombre del archivo externo (sin extensión .txt): ").strip()
    nombre_completo = nombre + ".txt"

    cant = 0
    try:
        arch = open(nombre_completo, "rt", encoding="utf-8")
        print(f"\n=== CONTENIDO DEL ARCHIVO: {nombre_completo} ===")
        for linea in arch:
            linea_limpia = linea.strip()
            if linea_limpia:
                objeto = json.loads(linea_limpia)
                print(objeto)
                cant += 1
        if cant == 0:
            print("[INFO] El archivo está vacío.")
    except FileNotFoundError:
        print(f"[ERROR] No se encontró el archivo '{nombre_completo}'.")
    except json.JSONDecodeError:
        print("[ERROR] El archivo contiene un formato JSON inválido.")
    except OSError as error:
        print(f"[ERROR] No se pudo leer el archivo: {error}")
    finally:
        try:
            arch.close()
        except NameError:
            pass


# ==========================================
# SUBMENÚS DE NAVEGACIÓN
# ==========================================

def sub_modo_consulta_contactos():
    """Submenú de búsquedas para la sección Contactos."""
    ejecutando = True
    while ejecutando:
        opciones = [
            "Buscar por ID",
            "Buscar por Nombre",
            "Buscar por Teléfono",
            "Buscar por Mail",
            "Buscar por Grupo",
            "Volver al menú de contactos"
        ]
        eleccion = menu_opciones("Contacto - Modo Consulta", opciones)
        match eleccion:
            case 1:
                id_buscado = pedir_entero("Ingrese ID a buscar: ")
                consultar_por_filtro("id", id_buscado, tipo_busqueda="igual",ruta_archivo="contactos.txt")
            case 2:
                nombre = input("Ingrese nombre o parte del nombre: ").strip()
                consultar_por_filtro("nombre", nombre, tipo_busqueda="subcadena",ruta_archivo="contactos.txt")
            case 3:
                tel = pedir_entero("Ingrese número de teléfono o parte de este: ")
                consultar_por_filtro("telefono", tel, tipo_busqueda="subcadena",ruta_archivo="contactos.txt")
            case 4:
                mail = input("Ingrese mail o parte del mail: ").strip()
                consultar_por_filtro("mail", mail, tipo_busqueda="subcadena",ruta_archivo="contactos.txt")
            case 5:
                grupo = seleccionar_grupo_desde_archivo()
                consultar_por_filtro("grupo", grupo, tipo_busqueda="igual",ruta_archivo="contactos.txt")
            case 6:
                ejecutando = False

def sub_modo_escritura_contactos():
    """Submenú de operaciones de modificación para la sección Contactos."""
    ejecutando = True
    while ejecutando:
        opciones = [
            "Agregar un contacto",
            "Modificar un contacto",
            "Eliminar un contacto",
            "Gestionar Papelera de Reciclaje",
            "Volver al menú de contactos"
        ]
        eleccion = menu_opciones("Contacto - Modo Escritura", opciones)
        match eleccion:
            case 1:
                agregar_contacto_archivo()
            case 2:
                modificar_contacto_archivo()
            case 3:
                eliminar_contacto_archivo()
            case 4:
                gestionar_papelera_archivo()
            case 5:
                ejecutando = False

def gestion_seccion_contactos():
    """Gestor principal de la sección Contactos."""
    ejecutando = True
    while ejecutando:
        opciones = [
            "Modo Consulta (Búsquedas)",
            "Modo Escritura (Altas, Bajas y Modificaciones)",
            "Volver al menú principal"
        ]
        eleccion = menu_opciones("Sección de Contactos", opciones)
        match eleccion:
            case 1:
                sub_modo_consulta_contactos()
            case 2:
                sub_modo_escritura_contactos()
            case 3:
                ejecutando = False

def sub_modo_consulta_grupos():
    """Submenú de búsquedas para la sección Grupos."""
    ejecutando = True
    while ejecutando:
        opciones = [
            "Buscar grupo por ID",
            "Buscar grupo por Nombre",
            "Buscar grupos por Nivel de Prioridad",
            "Volver al menú de grupos"
        ]
        eleccion = menu_opciones("Grupo - Modo Consulta", opciones)
        match eleccion:
            case 1:
                id_buscado = pedir_entero("Ingrese ID del grupo: ")
                consultar_por_filtro("id", id_buscado, tipo_busqueda="igual",ruta_archivo="grupos.txt")
            case 2:
                nombre = input("Ingrese nombre o parte del nombre del grupo: ").strip()
                consultar_por_filtro("nombre", nombre, tipo_busqueda="subcadena",ruta_archivo="grupos.txt")
            case 3:
                prioridades = ("Alta", "Media", "Baja")
                prio_sel = menu_opciones("Seleccionar Prioridad", prioridades)
                consultar_por_filtro("prioridad", prioridades[prio_sel - 1], tipo_busqueda="igual",ruta_archivo="grupos.txt")
            case 4:
                ejecutando = False

def sub_modo_escritura_grupos():
    """Submenú de operaciones de modificación para la sección Grupos."""
    ejecutando = True
    while ejecutando:
        opciones = [
            "Agregar un grupo",
            "Modificar un grupo",
            "Eliminar un grupo",
            "Volver al menú de grupos"
        ]
        eleccion = menu_opciones("Grupo - Modo Escritura", opciones)
        match eleccion:
            case 1:
                agregar_grupo_archivo()
            case 2:
                modificar_grupo_archivo()
            case 3:
                eliminar_grupo_archivo()
            case 4:
                ejecutando = False

def gestion_seccion_grupos():
    """Gestor principal de la sección Grupos."""
    ejecutando = True
    while ejecutando:
        opciones = [
            "Modo Consulta (Búsquedas y Lectura)",
            "Modo Escritura (Altas, Bajas y Modificaciones)",
            "Volver al menú principal"
        ]
        eleccion = menu_opciones("Sección de Grupos", opciones)
        match eleccion:
            case 1:
                sub_modo_consulta_grupos()
            case 2:
                sub_modo_escritura_grupos()
            case 3:
                ejecutando = False


# ==========================================
# MENÚ PRINCIPAL Y APLICACIÓN
# ==========================================

def main():
    """Función principal que dirige la navegación general de la agenda."""
    ejecutando = True
    opciones_main = [
        "Gestionar Contactos",
        "Gestionar Grupos",
        "Exportar Datos a Archivo",
        "Leer Archivo Externo",
        "Salir"
    ]

    while ejecutando:
        eleccion = menu_opciones("Sistema de Agenda de Contactos", opciones_main)
        match eleccion:
            case 1:
                gestion_seccion_contactos()
            case 2:
                gestion_seccion_grupos()
            case 3:
                exportar_archivo_secuencial()
            case 4:
                leer_archivo_externo()
            case 5:
                print("\n¡Gracias por utilizar el sistema de agenda! Saliendo...")
                ejecutando = False

main()
