cmake_minimum_required(VERSION 3.13)
project(attractmode_wrapper C)
include("${CMAKE_CURRENT_SOURCE_DIR}/../tools/kiosk_title.cmake")

add_executable(attractmode_wrapper
  src/main.c
  src/video_path.c
  src/player.c)

kiosk_package_title(attractmode_wrapper 1fa82100
  NAME "Attract Mode"
  SHORTNAME "Attract")
