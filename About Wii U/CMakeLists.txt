cmake_minimum_required(VERSION 3.13)
project(aboutwiiu_wrapper C)
include("${CMAKE_CURRENT_SOURCE_DIR}/../tools/kiosk_title.cmake")

add_executable(aboutwiiu_wrapper
  src/main.c
  src/video_path.c
  src/player.c)

kiosk_package_title(aboutwiiu_wrapper 1fa82000
  NAME "About Wii U"
  SHORTNAME "About")
