def pedir_entero(mensaje):
    entrada = input(mensaje)
    while not entrada.isdigit():
        print("[ERROR] El valor ingresado no es un número entero positivo válido.")
        entrada = input(mensaje)
    return int(entrada)

def validar_numero(mensaje, inicio, final):
    numero = pedir_entero(mensaje)
    while numero < inicio or numero > final:
        print(f"[ERROR] El número debe estar entre {inicio} y {final}.")
        numero = pedir_entero(mensaje)
    return numero

def mostrar_menu():
    ancho = 40
    linea = "=" * ancho
    
    print(linea)
    print(" "*8, "AGENDA DE CONTACTOS")
    print(linea)
    print("  [1] Agregar un contacto") #Tomi
    print("  [2] Modificar un contacto") #Yo
    print("  [3] Eliminar un contacto") #Bianca
    print("  [4] Ver todos los contactos") #Suarez
    print("  [5] Buscar contacto") #Carlos
    print("  [6] Salir")
    print(linea)
    
def crear_agenda():
    agenda = [
        [1, "Juan Perez", 1122334455, "juan@gmail.com", "Trabajo"],
        [2, "Maria Gomez", 1199887766, "maria@gmail.com", "Familia"],
        [3, "Lucas Silva", 1144556677, "lucas@gmail.com", "Amigos"]
    ]
    return agenda

def crear_grupos():
    return [
        [1, "Trabajo", "Compañeros de la oficina y jefes", "Alta"],
        [2, "Familia", "Parientes directos y cercanos", "Alta"],
        [3, "Amigos", "Amigos del club y facultad", "Media"],
        [4, "Varios", "Contactos ocasionales", "Baja"]
    ]

def menu_opciones(titulo, opciones):
    print(f"\n=== {titulo.upper()} ===")
    for i in range(len(opciones)):
        print(f"  [{i + 1}] {opciones[i]}")
    return validar_numero(f"Seleccione una opción (1-{len(opciones)}): ", 1, len(opciones))

def obtener_nombre_grupo(id_grupo, grupos):
    for i in range(len(grupos)):
        if grupos[i][0] == id_grupo:
            return grupos[i][1]
    return "Sin Grupo"

def seleccionar_grupo(grupos):
    print("GRUPOS DISPONIBLES")
    opciones_grupos = []
    for i in range(len(grupos)):
        info = f"{grupos[i][1]} (Prioridad: {grupos[i][3]}) - {grupos[i][2]}"
        opciones_grupos.append(info)
        
    opcion = menu_opciones("Seleccionar Grupo", opciones_grupos)
    return grupos[opcion - 1][1]

def convertidor_texto(texto):
    return str(texto).replace(" ", "").lower()

def buscar_por_nombre_o_id(dato, agenda):
    dato_limpio = convertidor_texto(str(dato))
    for i in range(len(agenda)):
        id_contacto = str(agenda[i][0])
        nombre_contacto = convertidor_texto(agenda[i][1])
        
        if dato_limpio == id_contacto or dato_limpio == nombre_contacto:
            return i
            
    return -1

def buscar_por_telefono(dato, agenda):
    for j in range(len(agenda)):
        if agenda[j][2] == dato:
            return j
    return -1

def buscar_por_gmail(dato, agenda):
    dato_limpio = convertidor_texto(str(dato))   
    for l in range(len(agenda)):
        if convertidor_texto(agenda[l][3]) == dato_limpio:
            return l
    return -1

def buscar_por_grupo(dato, agenda):
    dato_limpio = convertidor_texto(str(dato))
    encontrados = []
    for k in range(len(agenda)):
        if convertidor_texto(agenda[k][4]) == dato_limpio:
            encontrados.append(agenda[k])
    return encontrados

def mostrar_contacto(contacto):
    print(f"ID: {contacto[0]} | Nombre: {contacto[1]} | Tel: {contacto[2]} | Mail: {contacto[3]} | Grupo: {contacto[4]}")

def eleccion_de_busqueda(agenda, grupos):
    opciones_busqueda = [
        "Buscar por nombre o ID",
        "Buscar por número de teléfono",
        "Buscar por grupo",
        "Buscar por mail",
        "Volver al menú principal"
    ]
    
    forma_de_busqueda = menu_opciones("Opciones de Búsqueda", opciones_busqueda)

    if forma_de_busqueda == 1:
        dato = input("Ingresar nombre o ID a buscar: ")
        pos = buscar_por_nombre_o_id(dato, agenda)
        if pos == -1:
            print("\n[RESULTADO] Contacto no encontrado.")
        else:
            print("\n[RESULTADO] Contacto encontrado:")
            mostrar_contacto(agenda[pos])
        
    elif forma_de_busqueda == 2:
        dato = pedir_entero("Ingresar número de teléfono: ")
        pos = buscar_por_telefono(dato, agenda)
        if pos == -1:
            print("\n[RESULTADO] Contacto no encontrado.")
        else:
            print("\n[RESULTADO] Contacto encontrado:")
            mostrar_contacto(agenda[pos])
        
    elif forma_de_busqueda == 3:
        dato = seleccionar_grupo(grupos)
        encontrados = buscar_por_grupo(dato, agenda)
        if len(encontrados) == 0:
            print(f"\n[RESULTADO] No hay contactos registrados en el grupo '{dato}'.")
        else:
            print(f"\n[RESULTADO] Contactos encontrados en el grupo '{dato}' ({len(encontrados)}):")
            for contacto in encontrados:
                mostrar_contacto(contacto)
        
    elif forma_de_busqueda == 4:
        dato = input("Ingresar mail: ")
        pos = buscar_por_gmail(dato, agenda)
        if pos == -1:
            print("\n[RESULTADO] Contacto no encontrado.")
        else:
            print("\n[RESULTADO] Contacto encontrado:")
            mostrar_contacto(agenda[pos])
        
    elif forma_de_busqueda == 5:
        print("[INFO] Regresando al menú principal...")
        return

def cambiar_dato(informacion):
    agenda = informacion[0]
    pos = informacion[1]
    nuevo_valor = informacion[2]
    columna = informacion[3]
    
    agenda[pos][columna] = nuevo_valor
    print("[ÉXITO] Contacto modificado correctamente.")

def modificar(agenda, pos, grupos):
    opciones_modificar = ["Nombre", "Teléfono", "Mail", "Grupo", "Cancelar"]
    eleccion = menu_opciones("Menú de Modificación", opciones_modificar)
    
    informacion = []
    
    if eleccion == 1:
        valor = input("Dime el nuevo nombre: ")
        informacion = [agenda, pos, valor, 1]
    elif eleccion == 2:
        valor = pedir_entero("Dime el nuevo teléfono: ")
        informacion = [agenda, pos, valor, 2]
    elif eleccion == 3:
        valor = input("Dime el nuevo mail: ")
        informacion = [agenda, pos, valor, 3]
    elif eleccion == 4:
        id_grupo = seleccionar_grupo(grupos)
        informacion = [agenda, pos, id_grupo, 4]
    elif eleccion == 5:
        print("[INFO] Operación cancelada.")
        
    if len(informacion) > 0:
        cambiar_dato(informacion)
        
def elimPersona(agenda):
    data = input("Dime el nombre/id de la persona que quieres eliminar: ")
    pos = buscar_por_nombre_o_id(data, agenda)
    if pos == -1:
        print("Persona no encontrada!!")
    else:
        agenda.pop(pos)
        print("[ÉXITO] Contacto eliminado.")

def mostrarContactos(agenda, grupos):
    filas = len(agenda)
    
    print("\n --- CONTACTOS -----")
    for f in range(filas):
        for c in range(len(agenda[f])):
            print(f"{str(agenda[f][c]):<15}", end="")
        print()

    filas = len(grupos)
    print("\n --- GRUPOS -----")
    for f in range(filas):
        for c in range(len(grupos[f])):
            print(f"{str(grupos[f][c]):<15}", end="")
        print()  

def main():
    agenda = crear_agenda()
    grupos = crear_grupos()
    ejecutando = True
    
    opciones_main = [
        "Agregar un contacto",
        "Modificar un contacto",
        "Eliminar un contacto",
        "Ver todos los contactos",
        "Buscar contacto",
        "Salir"
    ]
    
    while ejecutando:
        eleccion = menu_opciones("Agenda de Contactos", opciones_main)
        if eleccion == 1:
            print("[Opción 1 seleccionada]") 
        elif eleccion == 2:
            print("[Opción 2 seleccionada]")
            dato = input("Dime el nombre de la persona que quieres modificar o su id: ")
            pos = buscar_por_nombre_o_id(dato, agenda)
            if pos == -1:
                print("Persona no encontrada!!")
            else:
                modificar(agenda, pos, grupos)
        elif eleccion == 3:
            print("[Opción 3 seleccionada]")
            elimPersona(agenda)
        elif eleccion == 4:
            print("[Opción 4 seleccionada]")
            mostrarContactos(agenda, grupos)
        elif eleccion == 5:
            print("[Opción 5 seleccionada]")
            eleccion_de_busqueda(agenda, grupos)
        elif eleccion == 6:
            print("¡Gracias por usar la agenda! Saliendo...")
            ejecutando = False

if __name__ == "__main__":
    main()