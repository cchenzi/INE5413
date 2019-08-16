from graph import Graph
import sys

if len(sys.argv) < 2:
    print('Please run as:')
    print('\tapp.py', 'IDENTIFICATION', 'DATASET')
    exit()

ID = sys.argv[1]
DATASET = sys.argv[2]
a = Graph(ID)
a.read_file(DATASET)


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

print(a.vertices)
print(a.neighbours)

ex_bfs = a.breadth_first_search('1')
# print(ex_bfs)
distance_dict = dict(zip(a.vertices, ex_bfs[0]))

ancestral_dict = dict(zip(a.vertices, ex_bfs[1]))
print('Distances: ', distance_dict)
print('Ancestrals: ', ancestral_dict)
max_distance = max(distance_dict.values())
print_bfs_result(distance_dict)