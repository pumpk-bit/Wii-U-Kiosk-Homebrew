#pragma once

#include <stdbool.h>
#include <stddef.h>

#define ABOUT_WIIU_TID 0x000500001FA82000ull
#define ABOUT_WIIU_VIDEO_COUNT 6

bool VideoPath_BuildIndex(int index, char *out, size_t outSize);
bool VideoPath_FromArgv(int argc, char **argv, char *out, size_t outSize);
