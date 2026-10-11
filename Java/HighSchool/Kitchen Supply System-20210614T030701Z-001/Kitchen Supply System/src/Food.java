import java.time.LocalDate;
import java.time.Period;
import java.time.format.DateTimeFormatter;

public class Food {
    private String Quantity;
    private String Name;
    private LocalDate ExpirationDate;

    public Food(String name, String quantity, LocalDate expirationDate) {
        Quantity = quantity;
        Name = name;
        ExpirationDate = expirationDate;
    }
    public Food(String name, String quantity, String expirationDate) {
        Quantity = quantity;
        Name = name;
        this.setExpirationDate(expirationDate); ;
    }
    public String getQuantity() {
        return Quantity;
    }

    public String getName() {
        return Name;
    }

    public LocalDate getExpirationDate() {
        return ExpirationDate;
    }

    public void setQuantity(String quantity) {
        Quantity = quantity;
    }

    public void setName(String name) {
        Name = name;
    }

    public void setExpirationDate(LocalDate expirationDate) {
        ExpirationDate = expirationDate;
    }
    public void setExpirationDate(String expirationDate){
        this.ExpirationDate=LocalDate.parse(expirationDate, DateTimeFormatter.ofPattern("dd/MM/yyyy"));
    }
    public int getDaysLeft(){
        LocalDate temp= LocalDate.now();
        Period period=Period.between(temp, this.ExpirationDate);
        return period.getDays();

    }
}
