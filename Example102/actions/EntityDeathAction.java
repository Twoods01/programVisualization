package actions;

import physics.*;
import entities.*;
import entity_super.EntityAnim;

public class EntityDeathAction
   implements Action
{
   private EntityAnim entity;

   public EntityDeathAction(EntityAnim entity)
   {
      this.entity = entity;
   }
   
   public void entAction(WorldModel world)
   {
      world.removeEntity(entity);
      return;
   }
}
