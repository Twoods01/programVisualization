
import java.lang.Thread;
class test {
    public static void main(String[] args) {
System.out.println("push main test " + Thread.currentThread().getId());
        branchTesting();
        nestedLoop();
        String numString = recursiveString(5);
        System.out.println(numString);
        int num = addNumbersInString(numString);
        System.out.println(num);
        nothing();
System.out.println("pop main test " + Thread.currentThread().getId());
    }

    public static void nestedLoop(){
System.out.println("push nestedLoop test " + Thread.currentThread().getId());
        int i = 0;
        int j = 0;
        while(i < 2){
System.out.println("branch 2");
            One();
            while(j < 3){
System.out.println("branch 4");
                Two();
                j++;
            }
            i++;
        }
System.out.println("branch 6");
System.out.println("pop nestedLoop test " + Thread.currentThread().getId());
    }

    public static void branchTesting(){
System.out.println("push branchTesting test " + Thread.currentThread().getId());
        int strLength = 1;
        if (false)
        {
System.out.println("branch 1");
System.out.println("pop branchTesting test " + Thread.currentThread().getId());
            return ;
        }

        else{

System.out.println("branch 2");
            if (Three() > 1 && One())
            {
System.out.println("branch 3");
                Four();
                if (true){
System.out.println("branch 4");
System.out.println("pop branchTesting test " + Thread.currentThread().getId());
                    return;
                }
                //problem area
                else if (Two())
                {

System.out.println("branch 6");
                    Five();
                    if (true){
System.out.println("branch 7");
System.out.println("pop branchTesting test " + Thread.currentThread().getId());
                        return ;
                    }

                }

            }
            if (One() && Two())
            {
System.out.println("branch 12");
                Six();
                if (true){
System.out.println("branch 13");
System.out.println("pop branchTesting test " + Thread.currentThread().getId());
                    return;
                }
            }


        }
System.out.println("branch 16");
System.out.println("pop branchTesting test " + Thread.currentThread().getId());
    }

    //public static void Start(){return;}
    public static void End(){
System.out.println("push End test " + Thread.currentThread().getId());
System.out.println("pop End test " + Thread.currentThread().getId());
        return;
    }
    public static boolean One(){
System.out.println("push One test " + Thread.currentThread().getId());
boolean __TEMP_VAR__ = true;
System.out.println("pop One test " + Thread.currentThread().getId());
return __TEMP_VAR__;
    }
    public static boolean Two(){
System.out.println("push Two test " + Thread.currentThread().getId());
boolean __TEMP_VAR__ = true;
System.out.println("pop Two test " + Thread.currentThread().getId());
return __TEMP_VAR__;
    }
    public static int Three(){
System.out.println("push Three test " + Thread.currentThread().getId());
int __TEMP_VAR__ = 1;
System.out.println("pop Three test " + Thread.currentThread().getId());
return __TEMP_VAR__;
    }
    public static void Four(){
System.out.println("push Four test " + Thread.currentThread().getId());
System.out.println("pop Four test " + Thread.currentThread().getId());
        return;
    }
    public static void Five(){
System.out.println("push Five test " + Thread.currentThread().getId());
System.out.println("pop Five test " + Thread.currentThread().getId());
        return;
    }
    public static void Six(){
System.out.println("push Six test " + Thread.currentThread().getId());
System.out.println("pop Six test " + Thread.currentThread().getId());
        return;
    }
    public static void Seven(){
System.out.println("push Seven test " + Thread.currentThread().getId());
System.out.println("pop Seven test " + Thread.currentThread().getId());
        return;
    }
    public static void Eight(){
System.out.println("push Eight test " + Thread.currentThread().getId());
System.out.println("pop Eight test " + Thread.currentThread().getId());
        return;
    }
    public static void Nine(){
System.out.println("push Nine test " + Thread.currentThread().getId());
System.out.println("pop Nine test " + Thread.currentThread().getId());
        return;
    }
    public static void Ten(){
System.out.println("push Ten test " + Thread.currentThread().getId());
System.out.println("pop Ten test " + Thread.currentThread().getId());
        return;
    }

    

    public static String recursiveString(int num){
System.out.println("push recursiveString test " + Thread.currentThread().getId());
        test();
        if(num == 0){
System.out.println("branch 1");
            int whoCares = 1;

            nothing();
String __TEMP_VAR__ = ((Integer)num).toString();
System.out.println("pop recursiveString test " + Thread.currentThread().getId());
return __TEMP_VAR__;
        }
        else if(num == 2){
System.out.println("branch 3");
String __TEMP_VAR__ = ((Integer)num).toString() + recursiveString(decrementNumber(num));
System.out.println("pop recursiveString test " + Thread.currentThread().getId());
return __TEMP_VAR__;
        }
        else if(num == 3){
System.out.println("branch 5");
            ((Integer)num).toString();
            if(num == 3){
System.out.println("branch 6");
                test();   
            }
            else{
System.out.println("branch 7");
                System.out.println("Yaa");
                if(num == 19){
System.out.println("branch 8");
                    nothing();
                }
                else{
System.out.println("branch 9");
                    System.out.println("Hello");
                }
            }
        }
        else if(num == 4){
System.out.println("branch 11");
            test();
        }
System.out.println("branch 13");
        test();
String __TEMP_VAR__ = "Hi";
System.out.println("pop recursiveString test " + Thread.currentThread().getId());
return __TEMP_VAR__;
    }

    public static int decrementNumber(int num){
System.out.println("push decrementNumber test " + Thread.currentThread().getId());
int __TEMP_VAR__ = num - 1;
System.out.println("pop decrementNumber test " + Thread.currentThread().getId());
return __TEMP_VAR__;
    }

    public static int addNumbers(int num1, int num2){
System.out.println("push addNumbers test " + Thread.currentThread().getId());
int __TEMP_VAR__ = num1 + num2;
System.out.println("pop addNumbers test " + Thread.currentThread().getId());
return __TEMP_VAR__;
    }

    public static int addNumbersInString(String s){
System.out.println("push addNumbersInString test " + Thread.currentThread().getId());
        int sum = 0;
        nothing();
        for(int i = 0; i < s.length(); i++){
System.out.println("branch 2");
            sum = addNumbers(sum, Character.getNumericValue(s.charAt(i)));
        }
System.out.println("branch 3");
int __TEMP_VAR__ = sum;
System.out.println("pop addNumbersInString test " + Thread.currentThread().getId());
return __TEMP_VAR__;
    }

    public static void nothing(){
System.out.println("push nothing test " + Thread.currentThread().getId());
        int i = 5;
        while(i > 0){
System.out.println("branch 2");
            i = decrementNumber(i);
        }
System.out.println("branch 3");
System.out.println("pop nothing test " + Thread.currentThread().getId());
    }

    public static void test(){
System.out.println("push test test " + Thread.currentThread().getId());
        System.out.println("Hello");
System.out.println("pop test test " + Thread.currentThread().getId());
    }
}