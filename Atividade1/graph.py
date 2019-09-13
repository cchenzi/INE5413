from graphviz import Graph as graph_draw


class Graph:
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

    def validate_edge(self, edge):
        if len(edge) != 2:
            return False

        for e in edge:
            if e not in self.vertices:
                return False

        if edge in self.edges:
            return False
        return True

    def validate_vertice(self, vertice):
        if vertice not in self.vertices:
            return False
        return True

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

    def num_vertices(self):
        return len(self.vertices)

    def num_edges(self):
        return len(self.edges)

    def get_degree(self, vertice):
        if not self.validate_vertice(vertice):
            print(vertice, "doesn't exist!")
            return 0
        return self.degrees[vertice]

    def has_edge(self, edge):
        return edge in self.edges

    def get_weight(self, edge):
        if edge in self.edges:
            return self.weights[edge]
        return float('inf')

    def get_neighbours(self, vertice):
        return self.neighbours[vertice]

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
        gr = graph_draw(comment='Graph', format='png', strict=True)
        for x in self.edges:
            gr.edge(self.vertices_names[x[0]], self.vertices_names[x[1]], label=str(self.weights[x]))
        gr.view(filename=filename, cleanup='True')

    def draw_ancestral_tree(self, ancestral, filename):
        aux = list(zip(list(ancestral), ancestral.values()))
        gr = graph_draw(comment='Graph', format='png', strict=True)
        for x in aux:
            gr.edge(str(x[0]), str(x[1]))
        gr.view(filename=filename, cleanup='True')

    def read_file(self, file_name):
        import re
        file = open(file_name, 'r')
        content = file.readlines()

        vertices_step = False
        edges_step = False

        r1 = re.compile("^(\d+)\s(.+)$")
        r2 = re.compile('([^\s]+)')

        for string in content:
            if "*vertices" in string:
                vertices_step = True
                continue
            if "*edges" in string:
                vertices_step = False
                edges_step = True
                continue
            if vertices_step:
                aux = r1.search(string)
                w1 = aux.group(1)
                w2 = aux.group(2)
                self.add_vertice(w1, w2)
            if edges_step:
                w1 = r2.findall(string)
                self.add_edges((w1[0], w1[1]), w1[2])
                self.add_edges((w1[1], w1[0]), w1[2])
