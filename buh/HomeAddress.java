package buh;
public class HomeAddress {
    private String street;
    private String city;
    private String postalCode;
    
    public HomeAddress(String street, String city, String postalCode) {
        this.street = street;
        this.city = city;
        this.postalCode = postalCode;
    }
    
    @Override
    public String toString() {
        return street + ", " + city + " " + postalCode;
    }
}