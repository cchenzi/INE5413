# from graphviz import Graph as graph_draw
from graph import Graph
from random import randrange
import heapq
import copy


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
        self.X = set()
        self.Y = set()

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

    def prim(self):
        non_visited = list(self.vertices)  # keep track of nodes visited
        current_node = non_visited.pop() # first node, any node works 

        min_heap = [] # stores the minimal weight as first
                        # min_heap is always used with heapq methods
        
        output_edges = [] 
        soma = 0

        while(len(non_visited) != 0):
            # input all edges of node added into min_heap
            for neighbour in self.neighbours[current_node]:
                edge = (neighbour, current_node)
                heapq.heappush(min_heap, 
                                    (self.get_weight(edge),
                                    edge) 
                                )
            
            # searches for a non-visited node with minimal weight
            while(True):
                weight, edge = heapq.heappop(min_heap)
                if (edge[0] in non_visited):
                    next_node = edge[0]
                    this_edge = edge
                    break
                if (edge[1] in non_visited):
                    next_node = edge[1]
                    this_edge = edge
                    break
            
            # saves the progress made
            soma += weight
            output_edges.append(this_edge)
            non_visited.remove(next_node)
            current_node = next_node

        return (soma, output_edges)

    def get_weight(self, edge):
        if edge in self.edges:
            return self.weights[edge]

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

    def bfs_hk(self, mate, D, vertices_aux):
        Q = []
        idx_null = vertices_aux.index("-1")
        for x in self.X:
            idx_x = vertices_aux.index(x)
            if mate[idx_x] == "-1":
                D[idx_x] = 0
                Q.append(x)
            else:
                D[idx_x] = float('inf')

        # verificar esse demonio
        D[idx_null] = float('inf')
        while Q != []:
            x = Q.pop()
            idx_x = vertices_aux.index(x)
            if D[idx_x] < D[idx_null]:
                for y in self.neighbours[x]:
                    idx_y = vertices_aux.index(y)
                    idx_mate_y = vertices_aux.index(mate[idx_y])

                    if D[idx_mate_y] == float('inf'):
                        D[idx_mate_y] = D[idx_x] + 1
                        Q.append(mate[idx_y])

        return D[idx_null] != float('inf')

    def dfs_hk(self, mate, x, D, vertices_aux):
        idx_x = vertices_aux.index(x)
        if x != "-1":
            for y in self.neighbours[x]:
                idx_y = vertices_aux.index(y)
                idx_mate_y = vertices_aux.index(mate[idx_y])
                if D[idx_mate_y] == D[idx_x] + 1:
                    if self.dfs_hk(mate, mate[idx_y], D, vertices_aux):
                        mate[idx_y] = x
                        mate[idx_x] = y
                        return True
            D[idx_x] = float('inf')
            return False
        return True

    def hopcroft_karp(self):
        aux_edges = copy.deepcopy(self.edges)
        
        self.add_vertice("-1","-1")
        for v in self.X:
            self.add_edges((v,"-1"),0)
        for v in self.Y:
            self.add_edges(("-1",v),0)
        vertices_aux = list(self.vertices)
        vertices_aux.sort()
        #print(vertices_aux)
        D = [float('inf') for x in vertices_aux]
        mate = ["-1" for x in vertices_aux]
        m = 0

        while self.bfs_hk(mate, D, vertices_aux):
            for x in self.X:
                idx_x = vertices_aux.index(x)
                if mate[idx_x] == "-1":
                    if self.dfs_hk(mate, x, D, vertices_aux):
                        m += 1
        mate.pop(0)
        self.vertices.remove('-1')
        self.edges = aux_edges
        mr = m - 1

        return (mr, mate)
