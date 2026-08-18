#pragma once

#include <stdbool.h>
#include <stddef.h>

#define ATTRACT_MODE_TID 0x000500001FA82100ull
#define ATTRACT_MODE_VIDEO_COUNT 12

bool VideoPath_BuildIndex(int index, char *out, size_t outSize);
bool VideoPath_FromArgv(int argc, char **argv, char *out, size_t outSize);
