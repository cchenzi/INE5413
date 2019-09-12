from graph import Graph
import view_aux as v_x
import sys
import os

def main():
    """Gets arguments from user, builds up the graph and calls menu"""

    if len(sys.argv) < 2:
        print('Please run as:')
        print('\tapp.py', 'IDENTIFICATION', 'DATASET')
        print()
        print('Example:')
        print('\tapp.py', '1', 'datasets/contem_ciclo.txt')
        exit()

    ID = sys.argv[1]
    DATASET = sys.argv[2]
    graph = Graph(ID)
    graph.read_file(DATASET)
    menu(graph)


def menu(graph):
    while True:
        os.system('clear')
        print('Graph:', graph.identification)
        print('Please select: ')
        print('1: Breadth First Search')
        print('2: Eulerian Cicle')
        print('3: Bellman-Ford Algorithm')
        print('4: Floyd-Warshall Algorithm')
        print('5: Print Vertices')
        print('6: Print Edges')
        print('7: Verify Edge (weight included)')
        print('8: Verify Vertice (neighbours and label included)')
        print('9: Draw Graph')
        print('0: Exit')
        sel = int(input())

        if sel == 0:
            print('Goodbye')
            break
        if sel == 1:
            v_x.sel_bfs(graph)
        if sel == 2:
            print('xD')
            input('Press enter to continue...')
        if sel == 3:
            v_x.sel_bfa(graph)
        if sel == 4:
            v_x.sel_floyd_warshall(graph)
        if sel == 5:
            print('Vertices names: ', graph.vertices_names)
            print('Size: ', len(graph.vertices_names))
            input('Press enter to continue...')
        if sel == 6:
            print('Edges: ', graph.edges)
            print('Size: ', len(graph.edges))
            input('Press enter to continue...')
        if sel == 7:
            v_x.sel_verify_edge(graph)
        if sel == 8:
            v_x.sel_verify_vertice(graph)
        if sel == 9:
            if graph.num_edges() > 50:
                print('Graph too long to draw!')
            else:
                print('Insert filename: ')
                filename = input()
                graph.draw(filename)


if __name__ == "__main__":
    main()