/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package graphcoloring;

import java.io.FileNotFoundException;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 *
 * @author twoods0129
 */
public class GraphColoring
{

    public static void main(String[] args)
    {
        GraphStart graph = new GraphStart();
        boolean connected = false;
        boolean bipartite = false;
        try
        {
            graph.readfile_graph(args[0]);
            connected = graph.check_connected();
            bipartite = graph.check_bipartite();
            System.out.printf("Graph (%d verticies, %d edges)", graph.nvertices, graph.nedges);
            if(!connected)
                System.out.printf(" Not");
            System.out.printf(" Connected, ");
            if(!bipartite)
                System.out.printf(" Not");
            System.out.println(" Bicolorable\n");
            
        } catch (FileNotFoundException ex)
        {
            Logger.getLogger(GraphColoring.class.getName()).log(Level.SEVERE, null, ex);
        }
    }
}