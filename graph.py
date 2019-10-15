class Graph:
    '''
    Base class for weighted graph G(V, E, w), where:
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
        pass

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

    def num_vertices(self):
        return len(self.vertices)

    def num_edges(self):
        return len(self.edges)

    def get_degree(self, vertice):
        pass

    def has_edge(self, edge):
        return edge in self.edges

    def get_weight(self, edge):
        if edge in self.edges:
            return self.weights[edge]
        return float('inf')

    def get_neighbours(self, vertice):
        return self.neighbours[vertice]

    def add_edges(self, edge, weight):
        pass

    def read_file(self, file_name, isDigraph):
        import re
        file = open(file_name, 'r')
        content = file.readlines()

        if isDigraph:
            break_input = "*arcs"
        else:
            break_input = "*edges"

        vertices_step = False
        edges_step = False

        r1 = re.compile("^(\d+)\s(.+)$")
        r2 = re.compile('([^\s]+)')

        for string in content:
            if "*vertices" in string:
                vertices_step = True
                continue
            if break_input in string:
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
