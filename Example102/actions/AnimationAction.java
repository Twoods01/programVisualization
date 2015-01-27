package actions;

import entities.*;
import entity_super.EntityAnim;
import physics.*;


public class AnimationAction
   implements Action
{
   private EntityAnim entity;
   private int repeatCount;
   
   public AnimationAction(EntityAnim entity, int repeatCount)
   {
      this.entity = entity;
      this.repeatCount = repeatCount;
   }
   
   public void entAction(WorldModel world)
   {    
      if (repeatCount != 1)
      {
         entity.nextImg();
         
         AnimationAction newAction = new AnimationAction(entity,
               Math.max(repeatCount - 1, 0));
         world.scheduleAction(newAction, entity.getAnimationRate());
      }
      return;
   }
}
