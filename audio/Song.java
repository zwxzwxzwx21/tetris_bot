package audio;

public class Song extends FileAudio {
    private final String artist;

    public Song(String title, double duration, String artist) {
        super(title, duration);
        this.artist = artist;
    }

    public String getArtist() { return artist; }

    @Override
    public String toString() {
        return super.toString() + String.format(" [artist: %s]", artist);
    }

    @Override
    public void play() {
        requestStartPlayback();
        System.out.println("PLAYING SONG -> " + getTitle() + " by " + artist +
                " (duration: " + String.format("%.2f", getDuration()) + ")");
    }

    @Override
    public void stop() {
        if (isCurrentlyPlaying()) {
            System.out.println("STOP SONG -> " + getTitle() + " by " + artist);
            clearCurrent();
        }
    }
}