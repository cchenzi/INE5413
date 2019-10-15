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

    def add_vertice(self, vertice, name):
        if vertice in self.vertices:
            return 0
        self.vertices.add(vertice)
        self.vertices_names[vertice] = name
        self.degrees[vertice] = 0
        self.neighbours[vertice] = set()
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
        for idx, vertice in enumerate(edge):
            aux = edge[(idx + 1) % 2]
            self.neighbours[vertice].add(aux)
            self.degrees[vertice] += 1

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

    def strongly_connected(self):
        pass

    def topological_sorting(self):
        pass

    # pode ser o prim tb
    def kruskal(self):
        pass
