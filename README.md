# pirunner

Tiny Project to control the raspberry pi task set from your browser.
Integrates with your web directory listings (separately) to allow you
to run multiple applications. Personal project, not meant to be used
anywhere as of now. Alpha quality.


## Goals
- Run audio, video, games from the browser
- Control current process by sending keystrokes from the browser
- Run a complete server of its own, perhaps?
    + As of now integrates with Apache web listings


## Known Issues

- Video playback fails if subtitles fail to download
- subliminal doesn't do hash based matches any more
- Killing vlc, cvlc, or omxplayer seems to be having issues
    + fceux dies easily with .terminate() though

## Over-Engineering

There is a lot of opportunity for over-engineering this.
I am inclined towards using a message queue to start/end
tasks, and maybe a separate taskrunner process as well.

Also need to convert it to a systemd service so it starts
at boot.

## License

Licensed uner [MIT License](http://nemo.mit-license.org).
