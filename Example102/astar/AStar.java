package astar;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.PriorityQueue;
import java.util.Comparator;
import java.util.HashMap;

import physics.*;
import entity_super.EntityPosn;

public class AStar
{
   private AStarNode source;
   private AStarNode target;
   
   private PriorityQueue<AStarNode> openSet;
   private ArrayList<AStarNode>     clsdSet;
   
   private HashMap<AStarNode, AStarNode> pathMap;
   
   private ArrayList<Point> path;
   
   public AStar()
   {     
      Comparator<AStarNode> compare = new AStarCompare();
      openSet = new PriorityQueue<AStarNode>(2, compare);
      
      clsdSet = new ArrayList<AStarNode>();
      
      pathMap = new HashMap<AStarNode, AStarNode>();
      
      path = new ArrayList<Point>();
   }
   
   public double heurCost(AStarNode node1, AStarNode node2)
   {
      return Math.sqrt((node1.getPos().xCoord() - node2.getPos().xCoord()) *(node1.getPos().xCoord() - node2.getPos().xCoord()) +(node1.getPos().yCoord() - node2.getPos().yCoord()) * (node1.getPos().yCoord() - node2.getPos().yCoord()));
   }
   
   public ArrayList<AStarNode> findValidNeighbors(AStarNode node,
         ArrayList<AStarNode> clsdset, WorldModel world)
   {
      Point pt = node.getPos();
      ArrayList<AStarNode> nodeLst = new ArrayList<AStarNode>();
      
      for (int dy = -1; dy < 2; dy++)
      {
         for (int dx = -1; dx < 2; dx++)
         {
            if (Math.abs(dy) != Math.abs(dx))
            {
               Point newPt = new Point(pt.xCoord() + dx, pt.yCoord() + dy);
               
               if (world.withinBounds(newPt) && !(world.isOccupied(newPt)))
               {
                    if (!clsdSet.contains(new AStarNode(newPt)))
                    {
                       nodeLst.add(new AStarNode(newPt));
                    }
               }
            }
         }
      }
      
      return nodeLst;
   }
   
   public ArrayList<Point> starPath(EntityPosn srcEnt, EntityPosn trgEnt,
         String trgType, WorldModel world)
   {   
      if (trgEnt.getName() != trgType)
      {
         ArrayList<Point> stayPut = new ArrayList<Point>();
         stayPut.add(srcEnt.getPosition());
         return stayPut;
      }
      
      source = new AStarNode(srcEnt.getPosition());
      target = new AStarNode(trgEnt.getPosition());
      
      source.setF(heurCost(source, target));
      openSet.add(source);
      
      pathMap.put(source, null);
      
      while (openSet.size() > 0)
      {
         AStarNode current = openSet.poll();

         
         if (current.getPos().adjacent(target.getPos()))
         {
            return reconstructPath(current);
         }
         
         clsdSet.add(current);
         
         ArrayList<AStarNode> neighs = findValidNeighbors(current, clsdSet,
               world);
         
         if (neighs.size() > 0)
         {
            for (AStarNode neighNode : neighs)
            {
               double tempG = current.getG() + 1;
               double tempF = tempG + heurCost(neighNode, target);               
               
               if (!clsdSet.contains(neighNode))
               {
                  boolean inList = false;
                  
                  Iterator<AStarNode> iterated = openSet.iterator();
                  while (iterated.hasNext())
                  {  
                       AStarNode updateNode = iterated.next();
                       if (neighNode.equals(updateNode))
                       {
                          inList = true;
                          neighNode.setG(updateNode.getG());
                          neighNode.setF(updateNode.getF());
                       }
                  }
            
                  if (inList && neighNode.getG() > tempG)
                  {
                     openSet.remove(neighNode);
                     neighNode.setG(tempG);
                     neighNode.setF(tempF);
                     openSet.add(neighNode);
                     pathMap.put(neighNode, current);
                  }
                  
                  if (!inList)
                  {
                     neighNode.setG(tempG);
                     neighNode.setF(tempF);
                     openSet.add(neighNode);
                     pathMap.put(neighNode, current);
                  }
               }
            }
         }
         
         

      }
      
      // didn't find the target
      ArrayList<Point> stayPut = new ArrayList<Point>();
      stayPut.add(srcEnt.getPosition());
      return stayPut;
   }
   

   private ArrayList<Point> reconstructPath(AStarNode current)
   {      
      if (pathMap.get(current) != null)
      {
         reconstructPath(pathMap.get(current));
         path.add(current.getPos());
         return path;
      }
      else
      {
         path.add(current.getPos());
         return path;
      } 
   }
   
}
