Sample NewReleases.xml for WUHB and the /vol/content fallback.

Kiosk Menu reads the live list from this title's meta folder on NAND:

  mlc:/usr/title/00050000/1fa82300/meta/NewReleases.xml

After a build, edit Release/1fa82300/meta/NewReleases.xml (the generator will not
overwrite it). Replace the placeholder title ID with a demo you have installed.
See docs/Title/NewReleases.MD.
