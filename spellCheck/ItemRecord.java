
/**
 * The "nodes" that make up a RecordBST, contains a string for the word,
 * and an int that tallies how many times that word appears
 * 
 * @author Taylor Woods
 * @version Program4
 */
public class ItemRecord
{
   public String word;
   public int tally;
   public ItemRecord left;
   public ItemRecord right;
   
   //Constructor
   public ItemRecord(String name)
   {
      word = name;
      tally = 0;
      left = null;
      right = null;
   }

   public void incTally()
   {
      tally++;
   }

   public ItemRecord moveLeft()
   {
      return left;
   }

   public void updateLeft(ItemRecord newItem){
      left = newItem;
   }

   public void updateRight(ItemRecord newItem){
      right = newItem;
   }

   public ItemRecord moveRight()
   {
      return right;
   }

   public boolean isNull()
   {
      return this == null;
   }
}
