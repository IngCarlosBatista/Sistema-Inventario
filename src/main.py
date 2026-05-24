import os
from conexion import crear_tablas
from inventario import registrar_producto, mostrar_stock, actualizar_stock, eliminar_producto

def limpiar_pantalla():
    """Limpia la terminal según el sistema operativo para mantener la UX limpia."""
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_menu():
    """Despliega la interfaz visual del sistema comercial."""
    print("\n=========================================")
    print("      📦 SISTEMA DE CONTROL DE INVENTARIO ")
    print("=========================================")
    print(" 1. Registrar nuevo producto")
    print(" 2. Mostrar stock actual")
    print(" 3. Actualizar cantidad (Entrada/Salida)")
    print(" 4. Eliminar producto")
    print(" 5. Salir")
    print("=========================================")

def main():
    crear_tablas()
    
    while True:
        limpiar_pantalla()
        mostrar_menu()
        
        opcion = input("Seleccione una opción (1-5): ").strip()
        
        if opcion == "1":
            limpiar_pantalla()
            print("--- REGISTRAR NUEVO PRODUCTO ---")
            nombre = input("Nombre del producto: ").strip()
            descripcion = input("Descripción: ").strip()
            
            try:
                cantidad = int(input("Cantidad inicial: "))
                precio = float(input("Precio unitario: "))
                stock_minimo = int(input("Stock mínimo de alerta (Enter para usar 5): ") or 5)
                
                registrar_producto(nombre, descripcion, cantidad, precio, stock_minimo)
            except ValueError:
                print("\n❌ Error: La cantidad, el precio y el stock mínimo deben ser números válidos.")
                
            input("\nPresione Enter para continuar...")
            
        elif opcion == "2":
            limpiar_pantalla()
            print("--- STOCK ACTUAL EN ALMACÉN ---")
            mostrar_stock()
            input("\nPresione Enter para continuar...")
            
        elif opcion == "3":
            limpiar_pantalla()
            print("--- ACTUALIZAR CANTIDAD (ENTRADA / SALIDA) ---")
            # Mostramos primero el stock para que el usuario vea los IDs disponibles
            hay_productos = mostrar_stock()
            
            if hay_productos:
                try:
                    id_p = int(input("\nDigite el ID del producto a modificar: "))
                    print("\nTipo de movimiento:")
                    print("1. Entrada (+) de mercancía")
                    print("2. Salida (-) de mercancía")
                    tipo = input("Seleccione (1-2): ").strip()
                    
                    if tipo not in ["1", "2"]:
                        print("\n❌ Opción de movimiento no válida.")
                    else:
                        cant_cambio = int(input("Cantidad de unidades: "))
                        if cant_cambio <= 0:
                            print("\n❌ La cantidad debe ser mayor a cero.")
                        else:
                            accion = "entrada" if tipo == "1" else "salida"
                            actualizar_stock(id_p, cant_cambio, accion)
                except ValueError:
                    print("\n❌ Error: Los IDs y cantidades deben ser números enteros.")
            input("\nPresione Enter para continuar...")
            
        elif opcion == "4":
            limpiar_pantalla()
            print("--- ELIMINAR PRODUCTO ---")
            hay_productos = mostrar_stock()
            
            if hay_productos:
                try:
                    id_p = int(input("\nDigite el ID del producto que desea ELIMINAR: "))
                    confirmacion = input(f"¿Está seguro de eliminar el producto ID {id_p}? (s/n): ").strip().lower()
                    
                    if confirmacion == 's':
                        eliminar_producto(id_p)
                    else:
                        print("\n❌ Operación cancelada por el usuario.")
                except ValueError:
                    print("\n❌ Error: El ID debe ser un número entero válido.")
            input("\nPresione Enter para continuar...")
            
        elif opcion == "5":
            print("\n¡Gracias por utilizar el sistema! Saliendo...")
            break
        else:
            print("\n❌ Opción no válida. Intente de nuevo.")
            input("\nPresione Enter para continuar...")

if __name__ == "__main__":
    main()