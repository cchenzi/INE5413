from graphviz import Graph as graph_draw
from graph import Graph
from random import randrange


class Undigraph(Graph):
    '''
    Base class for undirected and weighted graph G(V, E, w), where:
        V represents a set of vertices;
        E represents a list of edges;
        w represents a list of weights.
    '''
    def __init__(self, identification):
        self.identification = identification
        self.edges = []
        self.vertices = set()
        self.vertices_names = {}
        self.neighbours = {}
        self.weights = {}
        self.degrees = {}

    def add_vertice(self, vertice, name):
        if vertice in self.vertices:
            return 0
        self.vertices.add(vertice)
        self.vertices_names[vertice] = name
        self.degrees[vertice] = 0
        self.neighbours[vertice] = set()

    def add_edges(self, edge, weight):
        if not self.validate_edge(edge):
            print("Can't add ", edge, "to edges!")
            return 0
        self.edges.append(edge)
        self.weights[edge] = float(weight)
        for idx, vertice in enumerate(edge):
            aux = edge[(idx + 1) % 2]
            self.neighbours[vertice].add(aux)
            self.degrees[vertice] += 1

    def breadth_first_search(self, vertice):
        vertices_aux = list(self.vertices)
        C = [False for x in vertices_aux]
        D = [float('inf') for x in vertices_aux]
        A = [None for x in vertices_aux]
        C[vertices_aux.index(vertice)] = True
        D[vertices_aux.index(vertice)] = 0
        Q = []
        Q.append(vertice)
        while Q != []:
            u = Q.pop(0)
            neigh = self.get_neighbours(u)
            idx_u = vertices_aux.index(u)
            for v in neigh:
                idx_v = vertices_aux.index(v)
                if not C[idx_v]:
                    C[idx_v] = True
                    D[idx_v] = D[idx_u] + 1
                    A[idx_v] = u
                    Q.append(v)
        return D, A

    def searchEulirianSubcicle(self, v, C):
        Ciclo = [v]
        t = v
        while True:
            ver_nei = True
            for u in self.get_neighbours(v):
                index = self.edges.index((u,v))
                if C[index] == False:
                    ver_nei = False
                    C[index] = True
                    C[self.edges.index((v,u))] = True
                    v = u
                    Ciclo.append(v)
                    break
                    
            if ver_nei:
                return (False, None)
            if (v == t):
                break
        for x in Ciclo:
            for w in self.get_neighbours(x):
                if C[self.edges.index((x,w))] == False:
                    (r,Aux_ciclo) = self.searchEulirianSubcicle(x, C)
                    if r == False:
                        return (False, None)
                    else:
                        aux = Ciclo.index(x)+1
                        Ciclo = Ciclo[:Ciclo.index(x)] + Aux_ciclo + Ciclo[aux:]
        return (True, Ciclo)

    def hierholzer(self):
        vertices_aux = list(self.vertices)
        C = [False for e in self.edges]
        v = vertices_aux[randrange(len(vertices_aux))]
        (r, Ciclo) = self.searchEulirianSubcicle(v, C)
        if r == False:
            return (False, None)
        else:
            for e in C:
                if not(e):
                    return(False, None)
            return (True, Ciclo)

    def bellman_ford(self, vertice):
        vertices_aux = list(self.vertices)
        D = [float('inf') for x in vertices_aux]
        A = [None for x in vertices_aux]
        D[vertices_aux.index(vertice)] = 0

        for i in range(1, len(vertices_aux) - 1):
            for edge in self.edges:
                idx_u = vertices_aux.index(edge[0])
                idx_v = vertices_aux.index(edge[1])
                weight = self.weights[edge]
                if D[idx_v] > D[idx_u] + weight:
                    D[idx_v] = D[idx_u] + weight
                    A[idx_v] = edge[0]

        for edge in self.edges:
            idx_u = vertices_aux.index(edge[0])
            idx_v = vertices_aux.index(edge[1])
            weight = self.weights[edge]
            if D[idx_v] > D[idx_u] + weight:
                return False, [], []

        return True, D, A

    def floyd_warshall(self):
        vertices_aux = list(self.vertices)

        # dicts to get rid of ordenation problems
        distance = {x: {y: float('inf') for y in vertices_aux} for x in vertices_aux}

        # inicializing matrix
        for v in vertices_aux:
            distance[v][v] = 0.0
            for n in self.get_neighbours(v):
                # ((v,n)) creates edge manually
                distance[v][n] = self.get_weight((v, n))

        # run algorithm
        for p in vertices_aux:
            for v in vertices_aux:
                for w in vertices_aux:
                    if distance[v][w] > distance[v][p] + distance[p][w]:
                        distance[v][w] = distance[v][p] + distance[p][w]

        return distance

    def draw(self, filename):
        gr = graph_draw(comment='Undigraph', format='png', strict=True)
        for x in self.edges:
            gr.edge(self.vertices_names[x[0]], self.vertices_names[x[1]],
                    label=str(self.weights[x]))
        gr.view(filename=filename, cleanup='True')

    def draw_ancestral_tree(self, ancestral, filename):
        aux = list(zip(list(ancestral), ancestral.values()))
        gr = graph_draw(comment='Graph', format='png', strict=True)
        for x in aux:
            gr.edge(str(x[0]), str(x[1]))
        gr.view(filename=filename, cleanup='True')
