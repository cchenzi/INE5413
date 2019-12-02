# INE5413 Assignment: Graph Theory

## Available algorithms:

  * <b>Undirected Graph:</b>
  
        Breadth First Search, Hierlholzer, Bellman Ford, Floyd Warshall, Prim.
    
  * <b>Directed Graph:</b> 
  
        Strongly Connected, Topological Sorting. 

  * <b>Bipartite Graph:</b>
  
        Hopcroft Karp.
        

## Usage

<b>Positional arguments:</b>

    id           set graph identification
    dataset      set input data


<b>Optional arguments:</b>

    -h, --help   show help message and exit
    --digraph    set graph as digraph (default is undigraph)
    --arcs       set file separator as *arcs (default is *edges)
    --bipartite  set graph as a bipartite graph (it's a undigraph)

<b>Example: </b>

    app.py 1 datasets/contem_ciclo.txt
        or
    app.py 1 datasets/dirigido1.txt --digraph --arcs
        or
    app.py 1 datasets/pequeno.txt --bipartite

