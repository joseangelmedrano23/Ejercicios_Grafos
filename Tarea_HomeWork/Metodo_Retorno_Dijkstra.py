import heapq

def dijkstra_camino(grafo_ponderado, inicio, destino):
    """
    
    Ejecuta Dijkstra y retorna la distancia mínima y la lista ordenada de vértices.
    
    """
    distancias = {v: float('infinity') for v in grafo_ponderado.adj}
    padres = {v: None for v in grafo_ponderado.adj}
    distancias[inicio] = 0
    pq = [(0, inicio)]

    while pq:
        dist_actual, actual = heapq.heappop(pq)

        if actual == destino:
            break

        if dist_actual > distancias[actual]:
            continue

        for vecino, peso in grafo_ponderado.adj.get(actual, []):
            distancia = dist_actual + peso

            if distancia < distancias[vecino]:
                distancias[vecino] = distancia
                padres[vecino] = actual
                heapq.heappush(pq, (distancia, vecino))

    # Reconstruimos el camino desde 'destino' hacia atrás usando los padres
    
    camino = []
    paso = destino
    while paso is not None:
        camino.append(paso)
        paso = padres[paso]

    camino.reverse()

    if camino and camino[0] == inicio:
        return distancias[destino], camino
    return float('infinity'), []