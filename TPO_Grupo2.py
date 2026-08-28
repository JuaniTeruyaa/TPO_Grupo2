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
    agenda=[[1,"Juan Perez",1122334455,"juan@gmail.com","Trabajo"],
            [2,"Maria Gomez",1199887766,"maria@gmail.com","Familia"],
            [3,"Lucas Silva",1144556677,"lucas@gmail.com","Amigos"]]
    
    return agenda

def main():
    agenda=crear_agenda()
    menu = True
    while menu:
        mostrar_menu()
        eleccion = validar_numero("Seleccione una opción (1-6): ", 1, 6)
        
        if eleccion == 1:
            print("[Opción 1 seleccionada]") # --> Append al diccionario
        elif eleccion == 2:
            print("[Opción 2 seleccionada]") # --> edit diccionario
        elif eleccion == 3:
            print("[Opción 3 seleccionada]") # --> borrar del diccionario
        elif eleccion == 4:
            print("[Opción 4 seleccionada]") # --> Mosrtar como matriz?? 
        elif eleccion == 5:
            print("[Opción 5 seleccionada]") # Busquedas
        elif eleccion == 6:
            print("¡Gracias por usar la agenda! Saliendo...")
            menu = False

if __name__ == "__main__":
    main()
