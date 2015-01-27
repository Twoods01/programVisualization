
import java.io.File;
import java.util.Scanner;


/**
 * Short Description of Program.
 * 
 * @author Taylor
 * @version ProgramX
 */
public class SpellCheck
{
    public static final File dictionary = new File("unsortedWords.txt");
    public static RecordBST tree = new RecordBST(dictionary);
    public static RecordBST notFound = new RecordBST();
    
   public static void main(String args[])
   {

      
      try
      {
         File check = new File(args[0]);
         Scanner scan = new Scanner(check);
         while(scan.hasNext())
         {  
            ItemRecord look = new ItemRecord(scan.next());
            find(look);  
         }
      }
      catch(Exception e)
      {
         System.out.println(e.toString());
      }
      
      System.out.println("The file " + args[0] + " contained:");
      printFound();
      System.out.println("");
      System.out.println("These words were not found:");
      printNotFound();
   }
   
   public static void find(ItemRecord node)
   {
      ItemRecord p = tree.root;
      if(p.word.compareToIgnoreCase(node.word) == 0)
      {
         p.tally++;
         return;
      }
      while(p != null)
      {
         if(p.word.compareToIgnoreCase(node.word) < 0)
         {
            p = p.right;
         }
         else
         {
            p = p.left;
         }
         if(p == null)
         {
            notFound.place(node);
            return;
         }
         if(p.word.compareToIgnoreCase(node.word) == 0)
         {
            p.tally++;
            return;
         }
      }
      notFound.place(node);
      return;
   }
   
   public static void printFound()
   {
      private_printFound(tree.root);
   }
   
   private static void private_printFound(ItemRecord node)
   {
      if(node != null)
      { 
         private_printFound(node.left);
         if(node.tally > 0)
         {
            System.out.println(node.word + "   " + node.tally);
         }
         
         private_printFound(node.right);
      }
      return;
   }
   
   public static void printNotFound()
   {
      if(notFound.root != null)
      {
         private_printNotFound(notFound.root);
      }
   }
   
   private static void private_printNotFound(ItemRecord node)
   {
      if(node != null)
      { 
         private_printNotFound(node.left);
         System.out.println(node.word  + " Possible spellings: " + spellCheck(node));      
         private_printNotFound(node.right);
      }
   }
   
   private static boolean search(String word)
   {
      if(tree.root == null)
      {
         return false;
      }
      ItemRecord p = tree.root;
      
      if(p.word.compareToIgnoreCase(word) == 0)
      {
         return true;
      }
      while(p != null)
      {
         if(p.word.compareToIgnoreCase(word) < 0)
         {
            p = p.right;
         }
         else
         {
            p = p.left;
         }
         
         if(p == null)
         {
            return false;
         }
         if(p.word.compareToIgnoreCase(word) == 0)
         {
            return true;
         }
      }
      return false;
   }
   
   private static String spellCheck(ItemRecord node)
   {
      char[] wordArray = node.word.toCharArray();
      String temp;
      String possibleSpelling = "";
      for(int i = 0; i < wordArray.length - 1; i++)
      {
         swap(wordArray, i);
         temp = new String(wordArray);
         if(search(temp))
         {
            possibleSpelling = possibleSpelling.concat(temp);
         }
         swap(wordArray, i);
      }
      return  possibleSpelling;
   }
   
   private static void swap(char[] array, int location)
   {
      char temp = array[location + 1];
      array[location + 1] = array[location];
      array[location] = temp;
   }
}
