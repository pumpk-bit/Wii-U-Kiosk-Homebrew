#pragma once

#include <stdbool.h>
#include <stddef.h>

#define ABOUT_AMIIBO_TID 0x000500001FA83300ull
#define ABOUT_AMIIBO_VIDEO_COUNT 1

bool VideoPath_BuildIndex(int index, char *out, size_t outSize);
bool VideoPath_FromArgv(int argc, char **argv, char *out, size_t outSize);
