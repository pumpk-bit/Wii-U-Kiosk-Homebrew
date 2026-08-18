cmake_minimum_required(VERSION 3.13)
project(exhibition_wrapper C)
include("${CMAKE_CURRENT_SOURCE_DIR}/../tools/kiosk_title.cmake")

add_executable(exhibition_wrapper src/main.c)

kiosk_package_title(exhibition_wrapper 1fa82700
  NAME "Exhibition Mode"
  SHORTNAME "Exhibit")
