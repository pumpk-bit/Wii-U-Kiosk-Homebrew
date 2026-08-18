cmake_minimum_required(VERSION 3.13)
project(newreleases_wrapper C)
include("${CMAKE_CURRENT_SOURCE_DIR}/../tools/kiosk_title.cmake")

add_executable(newreleases_wrapper
  src/main.c
  src/featured.c)

kiosk_package_title(newreleases_wrapper 1fa82300
  NAME "New Releases"
  SHORTNAME "New")
