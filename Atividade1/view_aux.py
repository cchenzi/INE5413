def print_bfs_result(distance_dict):
    print_aux = {}
    for k, x in distance_dict.items():
        if x not in print_aux:
            print_aux[x] = []
            print_aux[x].append(k)
        else:
            print_aux[x].append(k)
    for k in sorted(list(print_aux)):
        print('{}: {}'.format(k, ','.join(print_aux[k])))


def print_bfa_result(v, ancestral_dict, distance_dict):
    print_aux = {}
    for k, x in ancestral_dict.items():
        path = []
        if x is None or x == v:
            path.append(v)
            if k not in path:  # gambiarra das tristes
                path.append(k)
            print_aux[k] = path
        else:
            while x != v:
                path.append(x)
                x = ancestral_dict[x]
                if x == v:
                    path.append(x)
                    break
            print_aux[k] = path[::-1]
            print_aux[k].append(k)
    print(print_aux)
    print(distance_dict)
    for k in sorted(list(print_aux)):
        print('{}: {}; d={}'.format(k, ','.join(print_aux[k]),
                                    distance_dict[k]))


def print_floyd_warshall(distance_dict):
    # print_aux = {}
    # for k, x in distance_dict.items():
    #     if x not in print_aux:
    #         print_aux[x] = []
    #         print_aux[x].append(k)
    #     else:
    #         print_aux[x].append(k)

    # ok isso eh um cadinho complexo
    # 1- outer sorted, ok
    # 2- inner key sorted, get value

    print('Floyd Warshall:')
    for outer_k in sorted(list(distance_dict)):
        print_aux = [str(v) for inner_k, v in sorted(distance_dict[outer_k].items())]
        print('{}: {}'.format(outer_k, ','.join(print_aux)))


def sel_bfs(graph):
    print('Please select a vertice: ', graph.vertices)
    v = input()
    bfs = graph.breadth_first_search(v)
    distance_dict = dict(zip(graph.vertices, bfs[0]))
    ancestral_dict = dict(zip(graph.vertices, bfs[1]))
    print('Distances: ', distance_dict)
    print('Ancestrals: ', ancestral_dict)
    # max_distance = max(distance_dict.values())
    print_bfs_result(distance_dict)
    print('Print ancestral tree? (y/n)')
    op = input()
    if op == 'y':
        print('Insert filename: ')
        filename = input()
        graph.draw_ancestral_tree(ancestral_dict, filename)
    input('Press enter to continue...')


def sel_bfa(graph):
    print('Please select a vertice: ', graph.vertices)
    v = input()
    bfa = graph.bellman_ford(v)
    if not bfa[0]:
        print("Can't find shortest path to", v)
    else:
        print(bfa[1])
        print(bfa[2])
        distance_dict = dict(zip(graph.vertices, bfa[1]))
        ancestral_dict = dict(zip(graph.vertices, bfa[2]))
        print('Distances: ', distance_dict)
        print('Ancestrals: ', ancestral_dict)
        print_bfa_result(v, ancestral_dict, distance_dict)
    input('Press enter to continue...')


def sel_floyd_warshall(graph):
    distances = graph.floyd_warshall()
    print_floyd_warshall(distances)

    # distance_dict = dict(zip(graph.vertices, distances))

    # print_bfs_result(distance_dict)

    # print(sorted(list(graph.vertices)))

    # print(graph.weights)

    # print()

    # print(graph.vertices)

    input('Press enter to continue...')


def sel_verify_vertice(graph):
    print('Please select a vertice: ', graph.vertices)
    v = input()
    if v in graph.vertices:  # arrumar esse print horroroso
        print("Vertice {}, name {}.\
        Neighbours: {}".format(v,
                               graph.vertices_names[v], graph.neighbours[v]))
    else:
        print('Vertice is not in graph!')
    input('Press enter to continue...')


def sel_verify_edge(graph):
    print('Edges: ', graph.edges)
    print('Please select a vertice: ', graph.vertices)
    v = input()
    print('Please select a vertice: ', graph.vertices)
    u = input()
    edge = (v, u)
    if graph.has_edge(edge):
        print("Edge {}. Weight = {}".format(edge, graph.weights[edge]))
    else:
        print('Edge is not in graph!')
    input('Press enter to continue...')
