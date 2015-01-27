package actions;

import java.util.HashMap;
import java.util.ArrayList;
import processing.core.*;
import java.util.Random;

import entities.*;
import physics.*;

public class VeinSpawnAction
   implements Action
{
   final static int VEIN_RATE_MIN = 8000;
   final static int VEIN_RATE_MAX = 17000;
   
   private Freeze freeze;
   private HashMap<String, ArrayList<PImage>> iStore;
   
   public VeinSpawnAction(Freeze freeze, HashMap<String, ArrayList<PImage>> iStore)
   {
      this.freeze = freeze;
      this.iStore = iStore;
   }
   
   public void entAction(WorldModel world)
   {
      Point veinPt = freeze.getPosition();
      
      world.removeEntity(freeze);
      
      Vein vein = createVein(world, veinPt);
      world.scheduleAction(new VeinAction(vein, iStore), vein.getRate());
      
      world.addEntity(vein);
      return; 
   }
   
   public Vein createVein(WorldModel world, Point pos)
   {
      Random rand = new Random();
      
      Vein vein = new Vein("vein", iStore.get("vein"), pos,
                           VEIN_RATE_MAX - rand.nextInt(VEIN_RATE_MIN));
      
      return vein;
   }
}
