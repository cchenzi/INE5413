from graph import Graph
import sys
import os

if len(sys.argv) < 2:
    print('Please run as:')
    print('\tapp.py', 'IDENTIFICATION', 'DATASET')
    exit()

ID = sys.argv[1]
DATASET = sys.argv[2]


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


def menu(graph):
    while True:
        os.system('clear')
        print('Graph:', graph.identification)
        print('Please select: ')
        print('1: Breadth First Search')
        print('2: Eulerian Cicle')
        print('3: Dijkstra Algorithm')
        print('4: Floyd-Warshall Algorithm')
        print('5: Print Vertices')
        print('6: Print Edges')
        print('7: Draw Graph')
        print('0: Exit')
        sel = int(input())

        if sel == 0:
            print('Goodbye')
            break
        if sel == 1:
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
                print('xD')
            input('Press enter to continue...')
        if sel == 2:
            print('xD')
            input('Press enter to continue...')
        if sel == 3:
            print('xD')
            input('Press enter to continue...')
        if sel == 4:
            print('xD')
            input('Press enter to continue...')
        if sel == 5:
            print('Vertices names: ', graph.vertices_names)
            input('Press enter to continue...')
        if sel == 6:
            print('Edges: ', graph.edges)
            input('Press enter to continue...')
        if sel == 7:
            if graph.num_edges() > 50:
                print('Graph too long to draw!')
            else:
                print('Insert filename: ')
                filename = input()
                graph.draw(filename)

graph = Graph(ID)
graph.read_file(DATASET)
menu(graph)
