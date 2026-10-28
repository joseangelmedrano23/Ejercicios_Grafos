import heapq

class SistemaNavegacionGPS:
    """
    
    Modela la red vial mediante un Grafo Ponderado representado por listas de adyacencia.
    - Vértices: Ciudades.
    - Aristas: Autopistas con peso asignado en minutos de viaje.
    
    """
    def __init__(self, dirigido=False):
        # Diccionario de adyacencia: {ciudad: [(vecino, tiempo_en_minutos), ...]}
        self.adj = {}
        # Indica si las autopistas son de doble vía (no dirigido) o de un solo sentido (dirigido)
        self.dirigido = dirigido

    def agregar_ciudad(self, ciudad):
        """
        Registra un nuevo nodo (ciudad) en el grafo si no existe previamente.
        Retorna True si fue agregada, o False si ya existía.
        """
        ciudad = ciudad.strip().title()
        if ciudad and ciudad not in self.adj:
            self.adj[ciudad] = []
            return True
        return False

    def agregar_autopista(self, origen, destino, tiempo):
        """
        Agrega una arista ponderada entre dos ciudades.
        Valida que el tiempo sea un valor numérico estrictamente positivo.
        """
        origen = origen.strip().title()
        destino = destino.strip().title()

        # Validación de caso límite: tiempo inválido
        if tiempo <= 0:
            raise ValueError("El tiempo de viaje debe ser mayor a 0 minutos.")

        # Validación de caso límite: bucles sobre el mismo nodo
        if origen == destino:
            raise ValueError("El origen y el destino no pueden ser la misma ciudad.")

        # Si las ciudades no existen, se agregan automáticamente
        self.agregar_ciudad(origen)
        self.agregar_ciudad(destino)

        # Se registra la conexión: (nodo_adyacente, peso)
        self.adj[origen].append((destino, tiempo))
        if not self.dirigido:
            self.adj[destino].append((origen, tiempo))

    def obtener_ciudades(self):
        """Retorna la lista de todas las ciudades registradas."""
        return list(self.adj.keys())

    def dijkstra_ruta_optima(self, origen, destino):
        """
        Calcula la ruta más rápida y el tiempo total entre dos ciudades
        utilizando el algoritmo de Dijkstra con cola de prioridad (min-heap)
        y reconstrucción mediante un diccionario de predecesores.
        """
        origen = origen.strip().title()
        destino = destino.strip().title()

        # Casos límite: existencia de las ciudades en el grafo
        if origen not in self.adj:
            raise KeyError(f"La ciudad de origen '{origen}' no está registrada en el sistema.")
        if destino not in self.adj:
            raise KeyError(f"La ciudad de destino '{destino}' no está registrada en el sistema.")

        # Si el origen es igual al destino
        if origen == destino:
            return 0, [origen]

        # Estructuras del algoritmo de Dijkstra
        # 1. Distancias acumuladas inicializadas en infinito
        tiempos = {ciudad: float('infinity') for ciudad in self.adj}
        tiempos[origen] = 0

        # 2. Diccionario de padres/predecesores para la reconstrucción del camino
        predecesores = {ciudad: None for ciudad in self.adj}

        # 3. Min-Heap ordenado por tiempo acumulado: (tiempo_acumulado, ciudad_actual)
        pq = [(0, origen)]

        while pq:
            tiempo_actual, ciudad_actual = heapq.heappop(pq)

            # Si alcanzamos el destino, podemos terminar antes (poda óptima)
            if ciudad_actual == destino:
                break

            # Poda de estados subóptimos: si el tiempo extraído es mayor que el registrado
            if tiempo_actual > tiempos[ciudad_actual]:
                continue

            # Relajación de aristas adyacentes
            for vecino, tiempo_tramo in self.adj.get(ciudad_actual, []):
                nuevo_tiempo = tiempo_actual + tiempo_tramo

                # Si encontramos un camino más rápido hacia 'vecino'
                if nuevo_tiempo < tiempos[vecino]:
                    tiempos[vecino] = nuevo_tiempo
                    predecesores[vecino] = ciudad_actual
                    heapq.heappush(pq, (nuevo_tiempo, vecino))

        # Reconstrucción del camino desde el destino hacia el origen
        camino = []
        paso = destino
        while paso is not None:
            camino.append(paso)
            paso = predecesores[paso]

        camino.reverse()

        # Si el camino no inicia en el origen, significa que no hay conexión posible
        if not camino or camino[0] != origen:
            return float('infinity'), []

        return tiempos[destino], camino


# ----------------------------------------------------------------------
# Interfaz de Usuario por Consola
# ----------------------------------------------------------------------

def precargar_datos_prueba(gps):
    """Carga una red básica inicial para facilitar las pruebas."""
    rutas_iniciales = [
        ("Madrid", "Segovia", 60),
        ("Madrid", "Toledo", 50),
        ("Madrid", "Zaragoza", 180),
        ("Segovia", "Valladolid", 75),
        ("Toledo", "Ciudad Real", 65),
        ("Zaragoza", "Barcelona", 190),
        ("Valladolid", "Burgos", 80),
        ("Burgos", "Zaragoza", 160)
    ]
    for origen, destino, tiempo in rutas_iniciales:
        gps.agregar_autopista(origen, destino, tiempo)


def menu():
    """Ejecuta el menú interactivo con validación de entradas y control de excepciones."""
    gps = SistemaNavegacionGPS(dirigido=False)
    precargar_datos_prueba(gps)

    while True:
        print("\n" + "=" * 45)
        print("     SISTEMA DE NAVEGACIÓN GPS (RUTAS)     ")
        print("=" * 45)
        print("1. Ver catálogo de ciudades registradas")
        print("2. Registrar una nueva ciudad")
        print("3. Registrar una nueva autopista / ruta")
        print("4. Consultar la ruta más rápida (Dijkstra)")
        print("5. Salir")
        print("=" * 45)

        opcion = input("Seleccione una opción (1-5): ").strip()

        if opcion == "1":
            ciudades = gps.obtener_ciudades()
            print("\n--- Ciudades en la Red ---")
            if not ciudades:
                print("No hay ciudades registradas.")
            else:
                for i, ciudad in enumerate(sorted(ciudades), start=1):
                    # Mostramos también cuántas conexiones directas tiene cada ciudad
                    conexiones = len(gps.adj[ciudad])
                    print(f"{i}. {ciudad} ({conexiones} autopistas conectadas)")

        elif opcion == "2":
            nueva_ciudad = input("\nIngrese el nombre de la nueva ciudad: ").strip()
            if not nueva_ciudad:
                print("Error: El nombre de la ciudad no puede estar vacío.")
            else:
                if gps.agregar_ciudad(nueva_ciudad):
                    print(f"Éxito: La ciudad '{nueva_ciudad.title()}' fue agregada.")
                else:
                    print(f"Aviso: La ciudad '{nueva_ciudad.title()}' ya formaba parte de la red.")

        elif opcion == "3":
            print("\n--- Registro de Nueva Autopista ---")
            origen = input("Ciudad de origen: ").strip()
            destino = input("Ciudad de destino: ").strip()

            try:
                tiempo_input = input("Tiempo estimado de viaje (minutos): ").strip()
                tiempo = float(tiempo_input)
                gps.agregar_autopista(origen, destino, tiempo)
                print(f"Éxito: Autopista conectada entre {origen.title()} y {destino.title()} ({tiempo} min).")
            except ValueError as err:
                # Manejo de excepciones para números no válidos o tiempos negativos/cero
                print(f"Error de validación: {err}")

        elif opcion == "4":
            print("\n--- Consulta de Ruta Óptima ---")
            origen = input("Ciudad de partida: ").strip()
            destino = input("Ciudad de llegada: ").strip()

            try:
                tiempo_total, ruta = gps.dijkstra_ruta_optima(origen, destino)

                if tiempo_total == float('infinity'):
                    print(f"\nResultado: No existe ninguna ruta viable entre {origen.title()} y {destino.title()}.")
                else:
                    print("\n" + "-" * 40)
                    print("         HOJA DE RUTA CALCULADA         ")
                    print("-" * 40)
                    print(f"Tiempo total estimado : {tiempo_total:.1f} minutos ({tiempo_total / 60:.2f} horas)")
                    print("Trayectoria detallada : " + " -> ".join(ruta))
                    print(f"Cantidad de tramos    : {len(ruta) - 1}")
                    print("-" * 40)

            except KeyError as err:
                # Manejo de ciudades no registradas
                print(f"Error en consulta: {err}")

        elif opcion == "5":
            print("\nCerrando el Sistema de Navegación GPS...")
            break

        else:
            print("Opción inválida. Por favor seleccione un número del 1 al 5.")


if __name__ == "__main__":
    menu() 