import javax.swing.Timer;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.time.Duration;
import java.util.Arrays;
import java.util.Scanner;
import java.util.function.Consumer;

class przyklady_funkcyjne {
    public static void main(String[] args) {
        student uczen = new student("kamil", "kowalski", "aaa001");
        pokaz_prezentacje_ucznia(uczen);

        prezentacja_zegara demo_zegara = new prezentacja_zegara();
        demo_zegara.uruchom_sluchacz_klasowy();
        demo_zegara.uruchom_sluchacz_lambda();

        pokaz_sortowanie_dni();
        uruchom_symulacje_gry();
    }

    private static void pokaz_prezentacje_ucznia(student uczen) {
        uczen.pokaz(dane -> System.out.println("widok prosty: " + dane.pobierz_nazwe()));
        uczen.pokaz(dane -> System.out.println("widok szczegolowy: " + dane));
        System.out.println();
    }

    private static void pokaz_sortowanie_dni() {
        System.out.println("sortowanie dni wedlug dlugosci");
        String[] dni = {"poniedzialek", "wtorek", "sroda", "czwartek", "piatek", "sobota", "niedziela"};
        Arrays.sort(dni, (lewy, prawy) -> Integer.compare(lewy.length(), prawy.length()));
        System.out.println("posortowane dni: " + String.join(", ", dni));
        System.out.println("lambda sortujaca implementuje comparator<string>");
        System.out.println();
    }

    private static void uruchom_symulacje_gry() {
        System.out.println("symulacja bohatera gry");
        bohater_gry bohater = new bohater_gry("lyra");

        try (Scanner czytnik = new Scanner(System.in)) {

            wykonawca_akcji silny_atak = new wykonawca_akcji() {
                @Override
                public String wykonaj_akcje(String cel) {
                    return "postac atakuje " + cel + " zadajac 50 pkt obrazen";
                }
            };

            wykonawca_akcji mikstura = cel -> "postac uzywa mikstury na " + cel + " odnawiajac 100 pkt zdrowia";

            wybieracz_celu wybor_uzytkownika = () -> {
                System.out.print("podaj cel: ");
                String dane = czytnik.nextLine();
                String bez_spacji = dane.trim();
                return bez_spacji.isEmpty() ? "nieznany cel" : bez_spacji.toLowerCase();
            };

            wybieracz_celu goblin = () -> "goblin";

            bohater.wykonaj_akcje(silny_atak, wybor_uzytkownika);
            bohater.wykonaj_akcje(mikstura, goblin);
        }
        System.out.println();
    }
}

interface osoba {
    default String pobierz_nazwe() {
        return "";
    }
}

interface nazwana {
    default String pobierz_nazwe() {
        return "";
    }
}

class student implements osoba, nazwana {
    private final String imie;
    private final String nazwisko;
    private final String numer_studenta;

    student(String imie, String nazwisko, String numer_studenta) {
        this.imie = imie;
        this.nazwisko = nazwisko;
        this.numer_studenta = numer_studenta;
    }

    @Override
    public String pobierz_nazwe() {
        return imie + " " + nazwisko;
    }

    public void pokaz(Consumer<student> sposob_prezentacji) {
        sposob_prezentacji.accept(this);
    }

    @Override
    public String toString() {
        return "student " + pobierz_nazwe() + ", numer " + numer_studenta;
    }
}

class prezentacja_zegara {
    public void uruchom_sluchacz_klasowy() {
        System.out.println("timer z klasy anonimowej");
        Timer timer = new Timer(5000, new licznik_czasu_sluchacz("demo listenera", 3));
        timer.setInitialDelay(0);
        timer.start();
        czekaj_na_zatrzymanie(timer);
        System.out.println();
    }

    public void uruchom_sluchacz_lambda() {
        System.out.println("timer z lambda");
        long start = System.nanoTime();
        final int maks_pulsow = 3;
        final int[] licznik = {0};

        Timer timer = new Timer(5000, zdarzenie -> {
            licznik[0]++;
            Duration czas = Duration.ofNanos(System.nanoTime() - start);
            System.out.println("lambda puls " + licznik[0] + " czas " + czas.getSeconds() + " s");
            if (licznik[0] >= maks_pulsow) {
                ((Timer) zdarzenie.getSource()).stop();
            }
        });

        timer.setInitialDelay(0);
        timer.start();
        czekaj_na_zatrzymanie(timer);
        System.out.println();
    }

    private void czekaj_na_zatrzymanie(Timer timer) {
        while (timer.isRunning()) {
            try {
                Thread.sleep(250);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                break;
            }
        }
    }

    private static class licznik_czasu_sluchacz implements ActionListener {
        private final long start = System.nanoTime();
        private final String opis;
        private final int maks_pulsow;
        private int puls;

        licznik_czasu_sluchacz(String opis, int maks_pulsow) {
            this.opis = opis;
            this.maks_pulsow = maks_pulsow;
        }

        @Override
        public void actionPerformed(ActionEvent zdarzenie) {
            puls++;
            Duration czas = Duration.ofNanos(System.nanoTime() - start);
            System.out.println(opis + " puls " + puls + " czas " + czas.getSeconds() + " s");
            if (puls >= maks_pulsow) {
                ((Timer) zdarzenie.getSource()).stop();
            }
        }
    }
}

interface wykonawca_akcji {
    String wykonaj_akcje(String cel);
}

interface wybieracz_celu {
    String wybierz_cel();
}

class bohater_gry {
    private final String nazwa;

    bohater_gry(String nazwa) {
        this.nazwa = nazwa;
    }

    public void wykonaj_akcje(wykonawca_akcji akcja, wybieracz_celu selektor) {
        String cel = selektor.wybierz_cel();
        String wynik = akcja.wykonaj_akcje(cel);
        System.out.println(nazwa + ": " + wynik);
    }
}
