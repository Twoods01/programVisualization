
class test {
    public static void main(String[] args) {
        branchTesting();
        nestedLoop();
        String numString = recursiveString(5);
        System.out.println(numString);
        int num = addNumbersInString(numString);
        System.out.println(num);
        nothing();
    }

    public static void nestedLoop(){
        int i = 0;
        int j = 0;
        if (One()) {
            while(i < 2){
                One();
                while(j < 3){
                    Two();
                    j++;
                }
                i++;
            }
        }
    }

    public static void branchTesting(){
        int strLength = 1;
        if (false)
            return ;
        else{

            if (Three() > 1 && One())
            {
                Four();
                if (true)
                    One();

                //problem area
                else if (Two())
                {

                    Five();
                    if (true)
                        return ;


                }

            }
            if (One() && Two())
            {
                Six();
                if (true){
                    return;
                }
            }


        }
    }

    //public static void Start(){return;}
    public static void End(){
        return;
    }
    public static boolean One(){
        return true;
    }
    public static boolean Two(){
        return true;
    }
    public static int Three(){
        return 1;
    }
    public static void Four(){
        return;
    }
    public static void Five(){
        return;
    }
    public static void Six(){
        return;
    }
    public static void Seven(){
        return;
    }
    public static void Eight(){
        return;
    }
    public static void Nine(){
        return;
    }
    public static void Ten(){
        return;
    }

    

    public static String recursiveString(int num){
        test();
        if(num == 0){
            int whoCares = 1;

            nothing();
            return ((Integer)num).toString();
        }
        else if(num == 2){
            return ((Integer)num).toString() + recursiveString(decrementNumber(num));
        }
        else if(num == 3){
            ((Integer)num).toString();
            if(num == 3){
                test();   
            }
            else{
                System.out.println("Yaa");
                if(num == 19){
                    nothing();
                }
                else{
                    System.out.println("Hello");
                }
            }
        }
        else if(num == 4){
            test();
        }
        test();
        return "Hi";
    }

    public static int decrementNumber(int num){
        return num - 1;
    }

    public static int addNumbers(int num1, int num2){
        return num1 + num2;
    }

    public static int addNumbersInString(String s){
        int sum = 0;
        nothing();
        for(int i = 0; i < s.length(); i++){
            sum = addNumbers(sum, Character.getNumericValue(s.charAt(i)));
        }
        return sum;
    }

    public static void nothing(){
        int i = 5;
        while(i > 0){
            i = decrementNumber(i);
        }
    }

    public static void test(){
        System.out.println("Hello");
    }
}