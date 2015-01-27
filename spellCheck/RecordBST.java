
import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;

/**
 * A binary search tree made up of ItemRecords, to hold
 * a dictionary.
 * 
 * @author Taylor Woods
 * @version Program4
 */
public class RecordBST
{
   public  ItemRecord root = null;
   
   public RecordBST()
   {
      
   }
   
   public RecordBST(File file)
   {
      try
      {
        Scanner scan = new Scanner(file);
        while(scan.hasNext())
        {
           ItemRecord node = new ItemRecord(scan.next());
           this.place(node);
         
        }
      } catch (Exception e)
      {
         System.out.println(e);
      }  
   }
   
   public void place(ItemRecord node)
   {
      if(this.root == null)
      {
         root = node;
      }
      else
      {
         ItemRecord p = root;
         while(p != null)
         {
            //Node word is less than or equal to p word
            if(node.word.compareToIgnoreCase(p.word) < 0)
            {
               if(p.left != null)
               {
                  p = p.left;
               }
               else
               {
                  p.left = node;
                  break;
               }
            }
            //Node word is greater than p word
            else
            {
               if(p.right != null)
               {
                  p = p.right;
               }
               else
               {
                  p.right = node;
                  break;
               }
            }
         }
         
   }
   
}  
   }
