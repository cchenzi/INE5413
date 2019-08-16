from graphviz import Graph as graph_draw


class Graph:
    '''
    Base class for undirected and weighted graph G(V, E, w), where:
        V represents a set of vertices;
        E represents a list of edges;
        w represents a list of weights.
    '''
 
    def __init__(self, identification):
        self.idetification = identification
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
        self.weights[edge] = weight
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
        for x in self.edges:
            if x == edge:
                return True
        return False

    def get_weight(self, edge):
        if edge in self.edges:
            return self.weights[edge]
        return float('inf')

    def get_neighbours(self, vertice):
        return self.neighbours[vertice]

    def breadth_first_search(self, vertice):
        vertices_aux = list(self.vertices)
        Cv = [False for x in vertices_aux]
        Dv = [float('inf') for x in vertices_aux]
        Av = [0 for x in vertices_aux]
        Cv[vertices_aux.index(vertice)] = True
        Dv[vertices_aux.index(vertice)] = 0
        Q = []
        Q.append(vertice)
        while Q != []:
            u = Q.pop(0)
            neigh = self.get_neighbours(u)
            idx_u = vertices_aux.index(u)
            for v in neigh:
                idx_v = vertices_aux.index(v)
                if not Cv[idx_v]:
                    Cv[idx_v] = True
                    Dv[idx_v] = Dv[idx_u] + 1
                    Av[idx_v] = u
                    Q.append(v)
        return Dv, Av

    def draw(self, filename):
        gr = graph_draw(comment='Graph', format='png', strict=True)
        for x in self.edges:
            gr.edge(self.vertices_names[x[0]], self.vertices_names[x[1]], label=self.weights[x])
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
