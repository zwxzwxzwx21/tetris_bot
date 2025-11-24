package audio;

public class Demo {
    public static void main(String[] args) {
        Song s1 = new Song("Song A", 210.0, "Artist X");
        Song s2 = new Song("Song B", 185.5, "Artist Y");
        Podcast p1 = new Podcast("Podcast 101", 3600.0, "Jane Doe");

        PlayList pl = new PlayList();
        pl.addElement(s1);
        pl.addElement(s2);
        pl.addElement(p1);

        System.out.println(pl);

        pl.playByTitle("Song A");
        pl.playByTitle("Podcast 101");
        pl.stopByTitle("Song B");
        pl.stopByTitle("Podcast 101");

        FileAudio found = FileAudio.findByTitle("Song B");
        if (found != null) {
            System.out.println("Globalnie znaleziono: " + found);
            found.play();
        }

        FileAudio.stopCurrent();
    }
}