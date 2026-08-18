cmake_minimum_required(VERSION 3.13)
project(title_list C)
include("${CMAKE_CURRENT_SOURCE_DIR}/../tools/kiosk_title.cmake")

add_executable(title_list
  src/main.c
  src/featured.c)

kiosk_package_title(title_list 1fa82200
  NAME "Featured List"
  SHORTNAME "Featured")
