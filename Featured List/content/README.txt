Sample Featured.xml for WUHB and the /vol/content fallback.

Kiosk Menu reads the live list from this title's meta folder on NAND:

  mlc:/usr/title/00050000/1fa82200/meta/Featured.xml

After a build, edit Release/1fa82200/meta/Featured.xml (the generator will not
overwrite it). Replace the placeholder title ID with a demo you have installed.
See docs/Title/FeaturedList.MD.
