package graphcoloring;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.util.Scanner;
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Collections;

// This is a very simple graph class,
// May get a compiler error due to use of array of ArrayLists
class GraphStart
{

    static final int MAXV = 100;
    static final int MAXDEGREE = 50;
    public boolean directed;
    public ArrayList<Integer>[] edges = new ArrayList[MAXV + 1];
    public int degree[] = new int[MAXV + 1];
    public int nvertices;
    public int nedges;

    GraphStart()
    {
        nvertices = nedges = 0;
        for (int i = 0; i <= MAXV; i++)
        {
            degree[i] = 0;
            edges[i] = new ArrayList<Integer>();
        }
    }

    void readfile_graph(String filename) throws FileNotFoundException
    {
        int x, y;
        FileInputStream in = new FileInputStream(new File(filename));
        Scanner sc = new Scanner(in);
        directed = (1 == sc.nextInt());      // 1 directed, anything else undirected
        nvertices = sc.nextInt();
        int m = sc.nextInt();                     // m is the number of edges in the file
        for (int i = 1; i <= m; i++)
        {
            x = sc.nextInt();
            y = sc.nextInt();
            insert_edge(x, y, directed);
        }
        // order edges (book convention) to ease debugging
        for (int i = 1; i <= nvertices; i++)
        {
            Collections.sort(edges[i]);
        }
    }

    void insert_edge(int x, int y, boolean directed)
    {
        // not worrying about capacity		         
        edges[x].add(y);
        degree[x]++;

        if (!directed)
        {       // adding "mirror" edge since not directed
            edges[y].add(x);
            degree[y]++;
            nedges++;
        }
    }

    void remove_edge(int x, int y)
    {
        if (degree[x] < 0)
        {
            System.out.println("Warning: no edge --" + x + ", " + y);
        }
        edges[x].remove((Integer) y);
        degree[x]--;
    }
    
    boolean check_bipartite()
    {
        ArrayDeque<Integer> queue = new ArrayDeque<Integer>();
        int[] colors = new int[nvertices + 1]; //+1 accounts for our verticies starting at 1
        
        //Initialize colors to -1
        for(int i = 0; i < nvertices + 1; i++)
            colors[i] = -1;
        
        //Check each vertex
        for (int i = 1; i <= nvertices; i++)
        {
            //If it hasn't been given a color, give it 1 and search 
            //through all it's children
            if (colors[i] == -1)
            {
                colors[i] = 1;
                //queue.push(i);
                queue.addFirst(i);

                while (!queue.isEmpty())
                {
                    //int parentVertex = queue.pop();
                    int parentVertex = queue.removeLast();
                    for (int j = 0; j < degree[parentVertex]; j++)
                    {
                        int childVertex = edges[parentVertex].get(j);
                        //If |childVertex| hasn't been colored yet, color it opposite
                        //of |currentVertex|, and add it to |queue|
                        if (colors[childVertex] == -1)
                        {
                            colors[childVertex] = 1 - colors[parentVertex];
                            //queue.push(childVertex);
                            queue.addFirst(childVertex);
                        } 
                        //If the child is colored the same as the parent
                        //the graph is not bipartite
                        else if (colors[childVertex] == colors[parentVertex])
                        {
                            return false;
                        }
                    }
                }
            }
        }
        
        return true;
    }
    
    boolean check_connected()
    {
        ArrayDeque<Integer> queue = new ArrayDeque<Integer>();
        int[] visited = new int[nvertices + 1]; //+1 accounts for our verticies starting at 1

        //Initialize visited to -1
        for (int i = 0; i < nvertices + 1; i++)
        {
            visited[i] = -1;
        }
        visited[1] = 1;
        //queue.push(1);
        queue.addFirst(1);

        while (!queue.isEmpty())
        {
            //int parentVertex = queue.pop();
            int parentVertex = queue.removeLast();
            for (int j = 0; j < degree[parentVertex]; j++)
            {
                int childVertex = edges[parentVertex].get(j);
                //If |childVertex| hasn't been visited yet mark it as visited
                //push it on the queue
                if (visited[childVertex] == -1)
                {
                    visited[childVertex] = 1;
                    //queue.push(childVertex);
                    queue.addFirst(childVertex);
                }
                
            }
        }
        for (int i = 1; i < nvertices + 1; i++)
        {
            if( visited[i] == -1)
                return false;
        }
        return true;
    }

    void print_graph()
    {
        if (directed)
        {
            System.out.printf("Directed Graph\n");
        } else
        {
            System.out.printf("Undirected Graph\n");
        }
        for (int i = 1; i <= nvertices; i++)
        {
            System.out.printf("%d: ", i);
            for (int j = 0; j <= degree[i] - 1; j++)
            {
                System.out.printf(" %d", edges[i].get(j));
            }
            System.out.printf("\n");
        }
    }
}