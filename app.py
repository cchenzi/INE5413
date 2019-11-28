# from graph import Graph
from undigraph import Undigraph
from digraph import Digraph
import view_aux as v_x
# import sys
import os
import argparse


def main():
    """Gets arguments from user, builds up the graph and calls menu"""

    text = "INE5413 Assignment: Graph Theory\n\
            Example: \n\
                app.py 1 datasets/contem_ciclo.txt\n\
            or\n\
                app.py 1 datasets/dirigido1.txt --digraph --arcs"
    # initiate the parser
    parser = argparse.ArgumentParser(description=text, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("id", help="set graph identification")
    parser.add_argument("dataset", help="set input data")
    parser.add_argument("--digraph",
                        help="set graph as digraph (default is undigraph)",
                        action="store_true")
    parser.add_argument("--arcs",
                        help="set file separator as *arcs (default is *edges)",
                        action="store_true")
    parser.add_argument("--bipartite",
                        help="set graph as a bipartite graph (it's a undigraph)",
                        action="store_true")

    # read arguments from the command line
    args = parser.parse_args()

    ID = args.id
    DATASET = args.dataset
    if args.digraph:
        graph = Digraph(ID)
    else:
        graph = Undigraph(ID)
    print(DATASET)
    graph.read_file(DATASET, args.arcs, args.digraph, args.bipartite)
    menu(graph, args.digraph)


def menu(graph, isDigraph):
    while True:
        os.system('clear')
        print('Graph:', graph.identification)
        print('Please select: ')
        print('1: Print Vertices')
        print('2: Print Edges')
        print('3: Verify Edge (weight included)')
        print('4: Verify Vertice (neighbours and label included)')
        print('5: Draw Graph')
        if (isDigraph):
            menu_digraph(graph)
        else:
            menu_undigraph(graph)
        sel = int(input())
        if sel == 0:
            print('Goodbye :)')
            break
        if sel == 1:
            print('Vertices names: ', graph.vertices_names)
            print('Size: ', len(graph.vertices_names))
            input('Press enter to continue...')
        if sel == 2:
            print('Edges: ', graph.edges)
            print('Size: ', len(graph.edges))
            input('Press enter to continue...')
        if sel == 3:
            v_x.sel_verify_edge(graph)
        if sel == 4:
            v_x.sel_verify_vertice(graph)
        if sel == 5:
            if graph.num_edges() > 50:
                print('Graph too long to draw!')
                input('Press enter to continue...')
            else:
                print('Insert filename: ')
                filename = input()
                graph.draw(filename)
        if (sel > 5 and sel <= 11):
            menu_aux(graph, isDigraph, sel)


def menu_aux(graph, isDigraph, sel):
    if isDigraph:
        if sel == 6:
            v_x.sel_scc(graph)
        if sel == 7:
            v_x.sel_tps(graph)
        if sel == 8:
            v_x.sel_edmonds_karp(graph)
    else:
        if sel == 6:
            v_x.sel_bfs(graph)
        if sel == 7:
            v_x.sel_hierholzer(graph)
        if sel == 8:
            v_x.sel_bfa(graph)
        if sel == 9:
            v_x.sel_floyd_warshall(graph)
        if sel == 10:
            v_x.sel_prim(graph)
        if sel == 11:
            v_x.sel_hk(graph)


def menu_digraph(graph):
    print('6: Strongly Connected Components')
    print('7: Topological Sorting')
    print('8: Edmonds-Karp Algorithm')
    print('0: Exit')


def menu_undigraph(graph):
    print('6: Breadth First Search')
    print('7: Eulerian Cicle')
    print('8: Bellman-Ford Algorithm')
    print('9: Floyd-Warshall Algorithm')
    print('10: Prim Algorithm')
    print('11: Hopcraft-Karp Algorithm')
    print('0: Exit')


if __name__ == "__main__":
    main()
