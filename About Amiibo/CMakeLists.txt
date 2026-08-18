cmake_minimum_required(VERSION 3.13)
project(aboutamiibo_wrapper C)
include("${CMAKE_CURRENT_SOURCE_DIR}/../tools/kiosk_title.cmake")

add_executable(aboutamiibo_wrapper
  src/main.c
  src/video_path.c
  src/player.c)

kiosk_package_title(aboutamiibo_wrapper 1fa83300
  NAME "About Amiibo"
  SHORTNAME "Amiibo")
