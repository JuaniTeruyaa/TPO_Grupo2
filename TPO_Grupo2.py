def validar_numero(mensaje, inicio, final):
    while True:
        try:
            numero = int(input(mensaje))
            assert inicio <= numero <= final, f"El número debe estar entre {inicio} y {final}."
            break
        except ValueError:
            print("[ERROR] El valor ingresado no es un número válido. Intente nuevamente.")
        except AssertionError as error:
            print(f"[ERROR] {error} Intente nuevamente.")
    return numero

def mostrar_menu():
    ancho = 40
    linea = "=" * ancho
    
    print(linea)
    print("AGENDA DE CONTACTOS".center(ancho))
    print(linea)
    print("  [1] Agregar un contacto")
    print("  [2] Modificar un contacto")
    print("  [3] Eliminar un contacto")
    print("  [4] Ver todos los contactos")
    print("  [5] Buscar contacto")
    print("  [6] Salir")
    print(linea)

def main():
    menu = True
    while menu:
        mostrar_menu()
        eleccion = validar_numero("Seleccione una opción (1-6): ", 1, 6)
        
        if eleccion == 1:
            print("[Opción 1 seleccionada]")
        elif eleccion == 2:
            print("[Opción 2 seleccionada]")
        elif eleccion == 3:
            print("[Opción 3 seleccionada]")
        elif eleccion == 4:
            print("[Opción 4 seleccionada]")
        elif eleccion == 5:
            print("[Opción 5 seleccionada]")
        elif eleccion == 6:
            print("¡Gracias por usar la agenda! Saliendo...")
            menu = False

if __name__ == "__main__":
    main()