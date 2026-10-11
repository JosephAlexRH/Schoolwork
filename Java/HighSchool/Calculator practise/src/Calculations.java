public class Calculations {
    double straightTimePayTotal;


    //Returns straightTimePay by multiplying the hourly rate by the hours worked
    public double straightTimePay(double hourlyRate, double hoursWorked){
        straightTimePayTotal=hourlyRate*hoursWorked;
        return straightTimePayTotal;
    }
    public double overtimePay(double overTimeMultiple, double hourlyRate, double hoursWorked){
        
    }


    public static void main(String[] args) {
        Calculations test=new Calculations();
        System.out.println(test.straightTimePay());
    }
}
