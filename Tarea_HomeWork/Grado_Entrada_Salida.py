def calcular_grados(grafo_dirigido):
    """
    
    Calcula in-degree y out-degree para cada vértice del grafo.
    
    """
    
    in_degree = {v: 0 for v in grafo_dirigido.adj}
    out_degree = {v: 0 for v in grafo_dirigido.adj}

    for u, lista_vecinos in grafo_dirigido.adj.items():
        out_degree[u] = len(lista_vecinos)
        for vecino in lista_vecinos:
            # Compatibilidad si la lista contiene tuplas (vecino, peso) o solo nombres de nodos
            destino = vecino[0] if isinstance(vecino, tuple) else vecino
            if destino in in_degree:
                in_degree[destino] += 1

    print(f"{'Vértice':<12} | {'Grado Entrada (In)':<20} | {'Grado Salida (Out)':<20}")
    print("-" * 56)
    for v in grafo_dirigido.adj:
        print(f"{v:<12} | {in_degree[v]:<20} | {out_degree[v]:<20}")