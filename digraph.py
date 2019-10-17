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

    def dfs_visit_ot(self, vertice, C, T, F, time, S, A):
        vertices_aux = list(self.vertices)
        C[vertices_aux.index(vertice)] = True
        time += 1
        T[vertices_aux.index(vertice)] = time
        for u in self.get_outneighbours(vertice):
            idx_u = vertices_aux.index(u)
            if not C[idx_u]:
                (C, T, F, time, S, A) = self.dfs_visit_ot(u, C, T, F, time, S, A)
        time += 1
        F[vertices_aux.index(vertice)] = time
        S.append(vertice)
        return (C, T, F, time, S, A)

    def topological_sorting(self):
        vertices_aux = list(self.vertices)
        C = [False for x in vertices_aux]  # visited
        T = [float('inf') for x in vertices_aux]  # visit_time
        F = [float('inf') for x in vertices_aux]  # finish_time
        A = [None for x in vertices_aux]  # Ancestral
        time = 0
        S = []  #
        for u in vertices_aux:
            idx_u = vertices_aux.index(u)
            if not C[idx_u]:
                (C, T, F, time, S, A) = self.dfs_visit_ot(u, C, T, F,
                                                          time, S, A)
        return S

    def strongly_connected(self):
        pass

    # pode ser o prim tb
    def kruskal(self):
        pass
