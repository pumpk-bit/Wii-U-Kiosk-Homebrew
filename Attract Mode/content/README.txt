User-supplied kiosk videos go on NAND in this title's meta folder, not here.

After a build, copy your own files to Release/1fa82100/meta/:

  AttractMode00.mp4
  ...
  AttractMode11.mp4

Then FTP that folder to:

  mlc:/usr/title/00050000/1fa82100/

Kiosk Menu scans meta/ and rotates through these clips in-menu for attract mode.
The wrapper accepts argv[1] = 0 .. 11 if the title is launched directly.
