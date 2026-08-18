User-supplied kiosk videos go on NAND in this title's meta folder, not here.

After a build, copy your own files to Release/1fa82100/meta/:

  AttractMode00.mp4
  ...
  AttractMode11.mp4

Then FTP that folder to:

  mlc:/usr/title/00050000/1fa82100/

The kiosk menu launches this title with argv[1] = 0 .. 11 (or AttractMode00 .. AttractMode11).
