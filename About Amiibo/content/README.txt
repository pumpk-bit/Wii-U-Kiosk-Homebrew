User-supplied kiosk video goes on NAND in this title's meta folder, not here.

After a build, copy your own file to:

  Release/1fa83300/meta/AboutAmiibo00.mp4

Then FTP that folder to:

  mlc:/usr/title/00050000/1fa83300/

Kiosk Menu reads this file from meta/ on MLC for in-menu playback. The wrapper
accepts argv[1] = 0 (or AboutAmiibo00) if the title is launched directly.
