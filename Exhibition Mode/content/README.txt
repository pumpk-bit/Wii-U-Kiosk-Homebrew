User-supplied exhibition videos go on NAND in this title's meta folder, not here.

After a build, copy paired clips to Release/1fa82700/meta/:

  TV00.mp4    (TV / HDMI output)
  DRC00.mp4   (GamePad output)
  TV01.mp4
  DRC01.mp4
  ...

TV and DRC counts must match. Slots are 00-99.

Then FTP to:

  mlc:/usr/title/00050000/1fa82700/

Enable Exhibition Mode in Kiosk Settings -> Set Menu Options.

Use tools/prepare_videos.py to copy/rename your source files into this layout. Or do it manually.
