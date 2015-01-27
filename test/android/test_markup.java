class test {
    public static void main(String[] args) {
System.out.println("push method main");
        String numString = recursiveString(5);
        System.out.println(numString);
        int num = addNumbersInString(numString);
        System.out.println(num);
        nothing();
    }

    public static String recursiveString(int num){
System.out.println("push method recursiveString");
        if(num == 0){
            int whoCares = 1;
String __TEMP_VAR__ = ((Integer)num).toString();
System.out.println("pop method recursiveString");
return __TEMP_VAR__;
        }
        else{
String __TEMP_VAR__ = ((Integer)num).toString() + recursiveString(decrementNumber(num));
System.out.println("pop method recursiveString");
return __TEMP_VAR__;
        }
    }

    public static int decrementNumber(int num){
System.out.println("push method decrementNumber");
int __TEMP_VAR__ = num - 1;
System.out.println("pop method decrementNumber");
return __TEMP_VAR__;
    }

    public static int addNumbers(int num1, int num2){
System.out.println("push method addNumbers");
int __TEMP_VAR__ = num1 + num2;
System.out.println("pop method addNumbers");
return __TEMP_VAR__;
    }

    public static int addNumbersInString(String s){
System.out.println("push method addNumbersInString");
        int sum = 0;
        nothing();
        for(int i = 0; i < s.length(); i++){
            sum = addNumbers(sum, Character.getNumericValue(s.charAt(i)));
        }
int __TEMP_VAR__ = sum;
System.out.println("pop method addNumbersInString");
return __TEMP_VAR__;
    }

    public static void nothing(){
System.out.println("push method nothing");
        int i = 5;
        while(i > 0){
            i = decrementNumber(i);
        }
System.out.println("pop method nothing");
        return;
    }
}