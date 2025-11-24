// Wszystkie klasy w jednym pliku dla wygody pokazania przykładu.
// W praktyce zwykle rozdzieliłbyś je do osobnych plików .java.

/**
 * Klasa abstrakcyjna opisująca wspólne cechy pliku audio (piosenka/podcast).
 * - Ma prywatne pola title, duration (jak wymagano).
 * - Przechowuje globalnie listę wszystkich utworów (registry), aby działało findByTitle(String).
 * - Trzyma statyczne pole currentlyPlaying do egzekwowania zasady: tylko jeden utwór gra naraz.
 */
abstract class FileAudio {
    // Prywatne pola według wymagań zadania
    private final String title;
    private final double duration; // w sekundach lub minutach (zależnie od przyjętej konwencji)

    // Globalny rejestr WSZYSTKICH utworów/podcastów (na potrzeby FileAudio.findByTitle(String))
    private static final java.util.List<FileAudio> registry = new java.util.ArrayList<>();

    // Jedyny aktualnie odtwarzany obiekt (egzekwowanie "gra tylko jeden naraz")
    private static FileAudio currentlyPlaying = null;

    protected FileAudio(String title, double duration) {
        this.title = title;
        this.duration = duration;

        // Każdy stworzony obiekt trafia do rejestru – dzięki temu findByTitle() ma gdzie szukać.
        registry.add(this);
    }

    // Gettery – przydatne w subclassach i do wyświetleń w toString()
    public String getTitle() { return title; }
    public double getDuration() { return duration; }

    /**
     * Wymagana w zadaniu metoda:
     * Szuka obiektu po tytule w globalnym rejestrze i zwraca pierwszy pasujący.
     * Zwraca null, jeśli nie znajdzie.
     *
     * Uwaga: utrzymujemy to w klasie FileAudio (zgodnie z treścią zadania),
     * aby można było wywołać FileAudio.findByTitle("...") niezależnie od playlisty.
     */
    public static FileAudio findByTitle(String title) {
        for (FileAudio f : registry) {
            if (f.getTitle().equalsIgnoreCase(title)) {
                return f;
            }
        }
        return null;
    }

    /**
     * Metoda pomocnicza – zgłoszenie chęci rozpoczęcia odtwarzania.
     * - Jeśli coś już gra, woła stop() na aktualnym obiekcie (żeby nie grały dwie rzeczy naraz).
     * - Ustawia "this" jako aktualnie grające.
     * - Nie drukuje komunikatu – to robią implementacje play() w subclassach, żeby wiadomo co gra.
     */
    protected final void requestStartPlayback() {
        if (currentlyPlaying != null && currentlyPlaying != this) {
            // Zatrzymaj to, co gra – to wywoła subclassowe stop(), które wydrukuje komunikat.
            currentlyPlaying.stop();
        }
        currentlyPlaying = this;
    }

    /**
     * Metoda pomocnicza – wołana zwykle z końca stop(), aby wyczyścić stan.
     */
    protected static final void clearCurrent() {
        currentlyPlaying = null;
    }

    /**
     * Czy ten obiekt jest obecnie odtwarzany?
     */
    protected final boolean isCurrentlyPlaying() {
        return currentlyPlaying == this;
    }

    /**
     * Czy cokolwiek aktualnie gra?
     */
    public static boolean isAnythingPlaying() {
        return currentlyPlaying != null;
    }

    /**
     * Zatrzymaj cokolwiek aktualnie gra globalnie (opcjonalne API pomocnicze).
     */
    public static void stopCurrent() {
        if (currentlyPlaying != null) {
            currentlyPlaying.stop(); // subclassowe stop() wyczyści current
        }
    }

    /**
     * Wymagane przez zadanie: ładne drukowanie informacji o pliku.
     * Zwracamy tytuł i czas trwania. (Formatowanie czasu – 2 miejsca po przecinku.)
     */
    @Override
    public String toString() {
        return String.format("%s (duration: %.2f)", title, duration);
    }

    // Metody abstrakcyjne wymagane przez zadanie – subclassy muszą je nadpisać.
    public abstract void play();
    public abstract void stop();
}

/**
 * Klasa reprezentująca piosenkę.
 * - Dziedziczy po FileAudio.
 * - Dodatkowe prywatne pole artist.
 * - Nadpisuje toString(), play(), stop().
 */
class Song extends FileAudio {
    private final String artist;

    public Song(String title, double duration, String artist) {
        super(title, duration);
        this.artist = artist;
    }

    public String getArtist() { return artist; }

    @Override
    public String toString() {
        // Do bazowego toString() dokładamy info o artyście.
        return super.toString() + String.format(" [artist: %s]", artist);
    }

    @Override
    public void play() {
        // Najpierw egzekwujemy zasadę: tylko jeden gra naraz:
        // jeśli coś gra, zostanie zatrzymane. Następnie ustawiamy siebie jako aktualnie grające.
        requestStartPlayback();

        // Teraz komunikat o rozpoczęciu odtwarzania:
        System.out.println("PLAYING SONG -> " + getTitle() + " by " + artist
                + " (duration: " + String.format("%.2f", getDuration()) + ")");
    }

    @Override
    public void stop() {
        if (isCurrentlyPlaying()) {
            // Zatrzymujemy tylko jeśli to my gramy (żeby nie drukować mylących komunikatów).
            System.out.println("STOP SONG -> " + getTitle() + " by " + artist);
            clearCurrent();
        } else {
            // Opcjonalny komunikat – nie jest wymagany, ale bywa pomocny w debugowaniu.
            System.out.println("STOP SONG (ignored, not playing) -> " + getTitle());
        }
    }
}

/**
 * Klasa reprezentująca podcast.
 * - Dziedziczy po FileAudio.
 * - Dodatkowe pole guest (gość).
 * - Nadpisuje toString(), play(), stop().
 */
class Podcast extends FileAudio {
    private final String guest;

    public Podcast(String title, double duration, String guest) {
        super(title, duration);
        this.guest = guest;
    }

    public String getGuest() { return guest; }

    @Override
    public String toString() {
        // Do bazowego toString() dokładamy info o gościu podcastu.
        return super.toString() + String.format(" [guest: %s]", guest);
    }

    @Override
    public void play() {
        // Egzekwowanie "jeden gra naraz".
        requestStartPlayback();

        // Komunikat o starcie odtwarzania podcastu:
        System.out.println("PLAYING PODCAST -> " + getTitle() + " with guest " + guest
                + " (duration: " + String.format("%.2f", getDuration()) + ")");
    }

    @Override
    public void stop() {
        if (isCurrentlyPlaying()) {
            System.out.println("STOP PODCAST -> " + getTitle() + " with guest " + guest);
            clearCurrent();
        } else {
            System.out.println("STOP PODCAST (ignored, not playing) -> " + getTitle());
        }
    }
}

/**
 * PlayList – przechowuje dowolne FileAudio (zarówno Song, jak i Podcast).
 * Zapewnia addElement/removeElement oraz wygodne metody odtwarzania po tytule.
 */
class PlayList {
    private final java.util.List<FileAudio> items = new java.util.ArrayList<>();

    // Dodanie elementu
    public void addElement(FileAudio audio) {
        if (audio != null) {
            items.add(audio);
        }
    }

    // Usunięcie elementu
    public boolean removeElement(FileAudio audio) {
        return items.remove(audio);
    }

    // Opcjonalne: wyszukiwanie w ramach tej playlisty (niezależnie od globalnego rejestru FileAudio)
    public FileAudio findByTitle(String title) {
        for (FileAudio f : items) {
            if (f.getTitle().equalsIgnoreCase(title)) {
                return f;
            }
        }
        return null;
    }

    // Wygodna metoda: odtwórz element z playlisty po tytule
    public boolean playByTitle(String title) {
        FileAudio f = findByTitle(title);
        if (f == null) return false;
        f.play(); // Zasada "jeden gra naraz" wyegzekwuje się automatycznie przez FileAudio.requestStartPlayback()
        return true;
    }

    // Wygodna metoda: zatrzymaj element z playlisty po tytule
    public boolean stopByTitle(String title) {
        FileAudio f = findByTitle(title);
        if (f == null) return false;
        f.stop();
        return true;
    }

    // Podgląd zawartości playlisty
    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder("PlayList:\n");
        for (int i = 0; i < items.size(); i++) {
            sb.append("  ").append(i + 1).append(". ").append(items.get(i).toString()).append("\n");
        }
        return sb.toString();
    }
}

/**
 * Prosty pokaz użycia – możesz uruchomić i zobaczyć działanie.
 * - Tworzy piosenki i podcasty
 * - Dodaje do playlisty
 * - Odtwarza po tytule, zatrzymuje, przełącza między utworami
 * (tylko jeden obiekt gra naraz – wymuszane w FileAudio)
 */
class Demo {
    public static void main(String[] args) {
        // Tworzymy przykładowe obiekty (trafiają do globalnego rejestru FileAudio)
        Song s1 = new Song("Song A", 210.0, "Artist X");
        Song s2 = new Song("Song B", 185.5, "Artist Y");
        Podcast p1 = new Podcast("Podcast 101", 3600.0, "Jane Doe");

        // Budujemy playlistę
        PlayList pl = new PlayList();
        pl.addElement(s1);
        pl.addElement(s2);
        pl.addElement(p1);

        System.out.println(pl);

        // Odtworzenie po tytule:
        pl.playByTitle("Song A");   // Zagra Song A
        pl.playByTitle("Podcast 101"); // Automatycznie zatrzyma Song A i włączy Podcast 101
        pl.stopByTitle("Song B");   // Ignorowane, bo Song B nie gra
        pl.stopByTitle("Podcast 101"); // Zatrzyma podcast

        // Globalne wyszukiwanie (niezależnie od playlisty) – działa przez rejestr FileAudio
        FileAudio found = FileAudio.findByTitle("Song B");
        if (found != null) {
            System.out.println("Globalnie znaleziono: " + found);
            found.play(); // Zagra Song B
        }

        // Zatrzymanie aktualnie grającego (globalnie)
        FileAudio.stopCurrent();
    }
}