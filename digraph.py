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
        self.inneighbours = {}

    def set_graph(self,edges, vertices,
            vertices_name, neighbours, weights, degrees, indegrees, outdegrees, outneighbours, inneighbours):
        self.edges = edges
        self.vertices = vertices
        self.vertices_names = vertices_name
        self.neighbours = neighbours
        self.weights = weights
        self.degrees = degrees
        self.indegrees = indegrees
        self.outdegrees = outdegrees
        self.outneighbours = outneighbours
        self.inneighbours = inneighbours


    def add_vertice(self, vertice, name):
        if vertice in self.vertices:
            return 0
        self.vertices.add(vertice)
        self.vertices_names[vertice] = name
        self.degrees[vertice] = 0
        self.neighbours[vertice] = set()
        self.outneighbours[vertice] = []
        self.inneighbours[vertice] = []
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
        self.inneighbours[edge[1]].append(edge[0])
        for idx, vertice in enumerate(edge):
            aux = edge[(idx + 1) % 2]
            self.neighbours[vertice].add(aux)
            self.degrees[vertice] += 1

    def get_outneighbours(self, vertice):
        return self.outneighbours[vertice]

    def get_inneighbours(self, vertice):
        return self.inneighbours[vertice]

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

    def dfs(self, vertices_aux):
        C = [False for x in vertices_aux]  # visited
        T = [float('inf') for x in vertices_aux]  # visit time
        F = [float('inf') for x in vertices_aux]  # finish time
        A = [None for x in vertices_aux]  # visited
        time = 0
        for v in vertices_aux:
            if not C[vertices_aux.index(v)]:
                time = self.dfs_visit(v,C,T,A,F,time, vertices_aux)
        return (C,T,A,F)
    
    def dfs_adaptad(self, Fl, vertices_aux):
        C = [False for x in vertices_aux]  # visited
        T = [float('inf') for x in vertices_aux]  # visit time
        F = [float('inf') for x in vertices_aux]  # finish time
        A = [None for x in vertices_aux]  # visited
        time = 0
        #Make copy to pick in reverse ordem without lost de index
        F_aux = Fl.copy()
        F_aux.sort(reverse = True)
        for f in F_aux:
            index_aux = Fl.index(f)
            v = vertices_aux[index_aux]
            if not C[index_aux]:
                time = self.dfs_visit(v,C,T,A,F,time, vertices_aux)
        return (C,T,A,F)

    def dfs_visit(self, v, C, T, A, F, time, vertices_aux):
        index = vertices_aux.index(v)
        C[index] = True
        time += 1
        T[index] = time
        for u in self.get_outneighbours(v):
            idx_u = vertices_aux.index(u)
            if not C[idx_u]:
                A[idx_u] = v
                time = self.dfs_visit(u, C, T, A, F, time, vertices_aux)
        time += 1
        F[index] = time
        return time

    def strongly_connected(self):
        #print(self.vertices)
        vertices_aux = list(self.vertices)
        vertices_aux.sort() # Isso porque por algum caso, vertices_aux nao estao em ordem de leitura, por isso, colocamos na ordem correta
        #Ja que é importante para validação
        #print(vertices_aux)
        (C, T, A, F) = self.dfs(vertices_aux)
        At = []
        Wt = {}
        for (v1,v2) in self.edges:
            At.append((v2,v1))
            Wt[(v2,v1)] = self.weights[(v1,v2)]
        graph_t = Digraph("T_aux")
        graph_t.set_graph(At, self.vertices, self.vertices_names, self.neighbours, Wt,
                            self.degrees, self.outdegrees, self.indegrees, self.inneighbours, self.outneighbours)
        #graph_t.draw("trans")
        (Ct, Tt, At_aux, Ft) = graph_t.dfs_adaptad(F, vertices_aux)
        return At_aux

    def residual_network(self, flow):
        # preguiça de fazer
        # edges_aux = self.edges
        # Af = []
        # capacity = {}
        # for edge in edges_aux:
        #   v = edge[0]
        #   u = edge[1]
        #   Af.append((v, u))
        #   capacity[(v, u)] = flow[edge]
        pass

    def edmonds_karp(self, source, target):
        vertices_aux = list(self.vertices)
        C = [False for x in vertices_aux]  # visited
        A = [None for x in vertices_aux]  # visited
        C[vertices_aux.index(source)] = True
        Q = []
        Q.append(source)
        while Q != []:
            path = []
            u = Q.pop()
            for v in self.get_outneighbours(u):
                idx_v = vertices_aux.index(v)
                if (not C[idx_v]) and (self.weights[(u, v)] - flow[(u, v)] > 0):
                    C[idx_v] = True
                    A[idx_v] = u

                    # ??
                    # if v == target:
                    #   path







