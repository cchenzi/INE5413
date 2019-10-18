from graphviz import Digraph as graph_draw
from graph import Graph
from random import randrange


class Digraph(Graph):
    '''
    Base class for directed and weighted graph G(V, E, w), where:
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
        self.indegrees = {}
        self.outdegrees = {}
        self.outneighbours = {}

    def add_vertice(self, vertice, name):
        if vertice in self.vertices:
            return 0
        self.vertices.add(vertice)
        self.vertices_names[vertice] = name
        self.degrees[vertice] = 0
        self.neighbours[vertice] = set()
        self.outneighbours[vertice] = []
        self.indegrees[vertice] = 0
        self.outdegrees[vertice] = 0

    def add_edges(self, edge, weight):
        if not self.validate_edge(edge):
            print("Can't add ", edge, "to edges!")
            return 0
        self.edges.append(edge)
        self.weights[edge] = float(weight)
        self.outdegrees[edge[0]] += 1
        self.indegrees[edge[1]] += 1
        self.outneighbours[edge[0]].append(edge[1])
        for idx, vertice in enumerate(edge):
            aux = edge[(idx + 1) % 2]
            self.neighbours[vertice].add(aux)
            self.degrees[vertice] += 1

    def get_outneighbours(self, vertice):
        return self.outneighbours[vertice]

    def get_degree(self, vertice):
        if not self.validate_vertice(vertice):
            print(vertice, "doesn't exist!")
            return 0
        return self.degrees[vertice]

    def get_indegree(self, vertice):
        if not self.validate_vertice(vertice):
            print(vertice, "doesn't exist!")
            return 0
        return self.indegrees[vertice]

    def get_outdegree(self, vertice):
        if not self.validate_vertice(vertice):
            print(vertice, "doesn't exist!")
            return 0
        return self.outdegrees[vertice]

    def is_balanced(self):
        for vertice in self.vertices:
            if (self.indegrees[vertice] != self.outdegrees[vertice]):
                return False
        return True

    def draw(self, filename):
        gr = graph_draw(comment='Digraph', format='png', strict=True)
        for x in self.edges:
            gr.edge(self.vertices_names[x[0]], self.vertices_names[x[1]],
                    label=str(self.weights[x]))
        gr.view(filename=filename, cleanup='True')

    def dfs_visit_ot(self, vertice, C, T, F, time, S, vertices_aux):
        C[vertices_aux.index(vertice)] = True
        time += 1
        T[vertices_aux.index(vertice)] = time
        for u in self.get_outneighbours(vertice):
            idx_u = vertices_aux.index(u)
            if not C[idx_u]:
                (C, T, F, time, S) = self.dfs_visit_ot(u, C, T, F, time, S,
                                                       vertices_aux)
        time += 1
        F[vertices_aux.index(vertice)] = time
        S.append(vertice)
        return (C, T, F, time, S)

    def topological_sorting(self):
        vertices_aux = list(self.vertices)
        C = [False for x in vertices_aux]  # visited
        T = [float('inf') for x in vertices_aux]  # visit time
        F = [float('inf') for x in vertices_aux]  # finish time
        time = 0
        S = []  # Topologically sorted vertices
        for u in vertices_aux:
            idx_u = vertices_aux.index(u)
            if not C[idx_u]:
                (C, T, F, time, S) = self.dfs_visit_ot(u, C, T, F,
                                                       time, S, vertices_aux)
        S.reverse()
        return S

    def dfs(self):
        vertices_aux = list(self.vertices)
        C = [False for x in vertices_aux]  # visited
        T = [float('inf') for x in vertices_aux]  # visit time
        F = [float('inf') for x in vertices_aux]  # finish time
        A = [None for x in vertices_aux]  # visited
        time = 0
        for v in vertices_aux:
            if not C[vertices_aux.index(v)]:
                self.dfs_visit(v,C,T,A,F,time)
        return (C,T,A,F)

    def dfs_visit(self, vertice, C, T, A, F, time)
        vertices_aux = list(self.vertices)
        index = vertices_aux.index(v)
        C[index] = True
        time += 1
        T[index] =time 
        for u in self.get_outneighbours(v):
            index_u = vertices_aux.index(u)
            if not C[index_u]:
                A[index_u] = v
                self.dfs_visit(u, C, T, A, F, time)
        time += 1
        F[index] = time


    def strongly_connected(self):
        pass

    # pode ser o prim tb
    def kruskal(self):
        pass
