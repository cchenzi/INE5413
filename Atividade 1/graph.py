class graph:
    def __init__(self, identification):
        self.indetification = identification
        self.edges = []
        self.vertices = set()
        self.vertices_names = {}  # o que vcs acham disso?
        self.weights = []
        self.degrees = {}

    def add_vertice(self, vertice, name):
        if vertice in self.vertices:
            return 0
        self.vertices.add(vertice)
        self.vertices_names[vertice] = name
        self.degrees[vertice] = 0

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
        self.weights.append(weight)

        for vertice in edge:
            self.degrees[vertice] += 1

    def num_vertices(self):
        return len(self.vertices)

    def num_edges(self):
        return len(self.edges)

    def get_degree(self, vertice):
        # manter um dict para os degrees, aumentando em cada acesso?
        if not self.validate_vertice(vertice):
            print(vertice, "doesn't exist!")
            return 0
        return self.degrees[vertice]
        '''
        degree = 0
        for edge in self.edges:
            if vertice in edge:
                degree += 1
        return degree
        '''

    def has_edge(self, edge):
        for x in self.edges:
            if x == edge:
                return True
        return False

    def get_weight(self, edge):
        count = 0
        for x in self.edges:
            if x == edge:
                return self.weights[count]
            count += 1
        return float('inf')

    def get_neighbours(self, vertice):
        aux = set(vertice)
        neighbours = []
        for edge in self.edges:
            if vertice in edge:
                neighbours.append(list(edge - aux)[0])
        return neighbours

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
                self.add_edges(set((w1[0], w1[1])), w1[2])
