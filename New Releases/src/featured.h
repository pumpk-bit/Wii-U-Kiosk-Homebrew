#pragma once

#include <coreinit/filesystem.h>
#include <stdbool.h>
#include <stdint.h>

#define FEATURED_MAX_TITLES 32

typedef struct FeaturedTitle {
   uint64_t titleId;
   int order;
   char startDate[32];
   char endDate[32];
} FeaturedTitle;

typedef struct FeaturedList {
   char type[32];
   int count;
   FeaturedTitle titles[FEATURED_MAX_TITLES];
} FeaturedList;

bool FeaturedList_Parse(const char *xml, FeaturedList *out);
bool FeaturedList_LoadPath(FSClient *client, FSCmdBlock *cmd, const char *path, FeaturedList *out);
