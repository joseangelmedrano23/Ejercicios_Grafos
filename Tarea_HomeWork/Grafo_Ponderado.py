from collections import deque
import heapq

class Grafo:
    """
    
    Representa un grafo no ponderado utilizando una lista de adyacencia
    
    """
    def __init__(self, dirigido=False):
        # Diccionario donde la clave es el vértice y el valor es la lista de vecinos
        self.adj = {}
        # Booleano que define si las aristas tienen una sola dirección o son bidireccionales
        self.dirigido = dirigido

    def agregar_vertice(self, v):
        """Añade un vértice al grafo si no existe previamente."""
        if v not in self.adj:
            self.adj[v] = []

    def agregar_arista(self, u, v):
        """
        
        Conecta el vértice u con el vértice v.
        Si alguno de los dos no existe en el grafo, se registra primero.
        
        """
        self.agregar_vertice(u)
        self.agregar_vertice(v)
        
        # Conexión dirigida: u -> v
        self.adj[u].append(v)
        
        # Si no es dirigido, la arista es bidireccional: v -> u
        if not self.dirigido:
            self.adj[v].append(u)

    def vecinos(self, v):
        """
        
        Devuelve la lista de nodos adyacentes a v.
        Retorna una lista vacía si el vértice no existe en el grafo.
        
        """
        return self.adj.get(v, [])


class GrafoPonderado(Grafo):
    """
    
    Hereda de Grafo para representar aristas que incluyen un peso o costo.
    En la lista de adyacencia, cada conexión se almacena como una tupla: (vecino, peso).
    
    """
    def __init__(self, dirigido=False):
        # Llama al constructor de la clase base (Grafo)
        super().__init__(dirigido)

    def agregar_arista(self, u, v, peso):
        """
        
        Sobrescribe el método de la clase padre para asociar un peso a la arista.
        
        """
        self.agregar_vertice(u)
        self.agregar_vertice(v)
        
        # Se almacena la tupla (nodo_destino, costo)
        self.adj[u].append((v, peso))
        if not self.dirigido:
            self.adj[v].append((u, peso))
            
    def vecinos(self, v):
        """
        
        Sobrescribe el método vecinos para devolver únicamente los identificadores
        de los nodos (descartando temporalmente los pesos), manteniendo compatibilidad
        con algoritmos como BFS o DFS.
        
        """
        return [vecino for vecino, peso in self.adj.get(v, [])]
        
    def dijkstra(self, inicio):
        """
        
        Calcula las distancias mínimas desde el vértice 'inicio' hacia todos
        los demás vértices alcanzables utilizando una cola de prioridad (min-heap).
        
        """
        # Paso 1: Inicialización
        # Todas las distancias empiezan en infinito, excepto el origen que vale 0
        distancias = {v: float('infinity') for v in self.adj}
        distancias[inicio] = 0
        
        # Cola de prioridad que almacena tuplas ordenadas por costo: (distancia_acumulada, vertice)
        pq = [(0, inicio)]
        
        # Paso 2: Bucle principal mientras existan nodos por procesar en la cola
        while pq:
            # Extraemos el nodo con la menor distancia acumulada actual (operación O(log V))
            dist_actual, actual = heapq.heappop(pq)
            
            # Optimización (poda): Si ya encontramos una ruta más corta previamente
            # para este nodo, descartamos esta entrada obsoleta del heap
            if dist_actual > distancias[actual]:
                continue
                
            # Paso 3: Relajación de aristas
            # Exploramos todos los vecinos del nodo actual con sus respectivos pesos
            for vecino, peso in self.adj.get(actual, []):
                distancia = dist_actual + peso
                
                # Si encontramos un camino más corto hacia 'vecino', actualizamos su distancia
                if distancia < distancias[vecino]:
                    distancias[vecino] = distancia
                    # Se inserta en la cola de prioridad con la nueva distancia tentativa
                    heapq.heappush(pq, (distancia, vecino))
                    
        # Retorna el diccionario final con las distancias más cortas calculadas
        return distancias


# --- Ejecución del Ejercicio 3 ---
red_trafico = GrafoPonderado(dirigido=False)

red_trafico.agregar_arista('Router_Central', 'Switch_A', 10)
red_trafico.agregar_arista('Router_Central', 'Switch_B', 25)
red_trafico.agregar_arista('Switch_A', 'Servidor_Datos', 30)
red_trafico.agregar_arista('Switch_A', 'Switch_B', 5)
red_trafico.agregar_arista('Switch_B', 'Servidor_Datos', 12)

latencias = red_trafico.dijkstra('Router_Central')

print("Menor latencia desde 'Router_Central':")
for nodo, latencia in latencias.items():
    print(f"  Hacia {nodo}: {latencia} ms")