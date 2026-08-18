# Shared packaging for kiosk titles. Include from each title CMakeLists.txt
# after project() so the Wii U toolchain has loaded wut_create_rpx.

if(NOT COMMAND wut_create_rpx)
  message(FATAL_ERROR
    "Configure this project with powerpc-eabi-cmake (devkitPro wut), not plain cmake.\n"
    "  bash tools/check-toolchain.sh\n"
    "  bash tools/build-all.sh\n"
    "powerpc-eabi-cmake lives in \$DEVKITPRO/portlibs/wiiu/bin on current installs.\n"
    "See docs/HowToBuild.MD")
endif()

function(kiosk_package_title target unique_id)
  cmake_parse_arguments(KIOSK "" "NAME;SHORTNAME;AUTHOR" "" ${ARGN})
  if(NOT KIOSK_AUTHOR)
    set(KIOSK_AUTHOR "Wii-U-Kiosk-Homebrew")
  endif()
  if(NOT KIOSK_SHORTNAME)
    set(KIOSK_SHORTNAME "${KIOSK_NAME}")
  endif()

  wut_create_rpx(${target})

  # .wuhb is optional. Kiosk FTP only needs the RPX in Release/. Older wut
  # shipped wut_create_wuhb; current dkp CMake may not.
  if(COMMAND wut_create_wuhb AND KIOSK_NAME)
    find_program(_KIOSK_WUHBTOOL NAMES wuhbtool wuhbtool.exe)
    if(_KIOSK_WUHBTOOL AND EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/content")
      wut_create_wuhb(${target}
        CONTENT "${CMAKE_CURRENT_SOURCE_DIR}/content"
        NAME "${KIOSK_NAME}"
        SHORTNAME "${KIOSK_SHORTNAME}"
        AUTHOR "${KIOSK_AUTHOR}")
    else()
      message(STATUS "Skipping .wuhb for ${target} (wuhbtool not found). RPX/FTP still built.")
    endif()
    unset(_KIOSK_WUHBTOOL)
  endif()

  set(_release "${CMAKE_CURRENT_SOURCE_DIR}/../Release/${unique_id}")
  add_custom_command(TARGET ${target} POST_BUILD
    COMMAND "${CMAKE_COMMAND}" -E make_directory "${_release}/code"
    COMMAND "${CMAKE_COMMAND}" -E copy_if_different
      "$<TARGET_FILE_DIR:${target}>/${target}.rpx"
      "${_release}/code/${target}.rpx"
    COMMENT "Copy ${target}.rpx to Release/${unique_id}/code/")

  find_program(_KIOSK_PYTHON NAMES python3 python python3.exe python.exe)
  if(_KIOSK_PYTHON)
    add_custom_command(TARGET ${target} POST_BUILD
      COMMAND "${_KIOSK_PYTHON}"
        "${CMAKE_CURRENT_SOURCE_DIR}/../tools/generate_title_xml.py"
        "--project" "${CMAKE_CURRENT_SOURCE_DIR}"
      COMMENT "Generate Cafe XML for ${unique_id}")
  else()
    message(WARNING "Python not found; after the build run: python3 tools/generate_title_xml.py")
  endif()
  unset(_KIOSK_PYTHON)
endfunction()
