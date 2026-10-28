def dfs_iterativo(grafo, inicio):
    """
    Recorrido DFS iterativo usando una Pila (Stack) y un conjunto de visitados.
    
    """
    visitados = set()
    pila = [inicio]
    resultado = []

    while pila:
        vertice = pila.pop()

        if vertice not in visitados:
            visitados.add(vertice)
            resultado.append(vertice)

            # Invertimos los vecinos para mantener el mismo orden de visita que el DFS recursivo
            for vecino in reversed(grafo.vecinos(vertice)):
                if vecino not in visitados:
                    pila.append(vecino)

    return resultado