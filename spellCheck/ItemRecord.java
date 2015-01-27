
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
}
