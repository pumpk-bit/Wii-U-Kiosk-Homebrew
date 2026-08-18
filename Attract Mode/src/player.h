#pragma once

#include <stdbool.h>

/* Play an MP4 from meta/. Returns true if playback finished normally. */
bool Video_Play(const char *path);
