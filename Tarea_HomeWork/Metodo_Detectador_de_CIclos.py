def tiene_ciclo(grafo_dirigido):
    """
    
    Detecta si existe al menos un ciclo en un grafo dirigido usando DFS.
    
    """
    visitados = set()
    camino_actual = set()

    def dfs(vertice):
        visitados.add(vertice)
        camino_actual.add(vertice)

        for vecino in grafo_dirigido.vecinos(vertice):
            # Si el vecino ya está en la ruta que estamos explorando, hay un ciclo
            if vecino in camino_actual:
                return True
            if vecino not in visitados:
                if dfs(vecino):
                    return True

        # Al retroceder (backtracking), lo quitamos del camino activo
        camino_actual.remove(vertice)
        return False

    # Verificamos todos los vértices en caso de que el grafo no sea conexo
    for vertice in grafo_dirigido.adj:
        if vertice not in visitados:
            if dfs(vertice):
                return True
            
    return False