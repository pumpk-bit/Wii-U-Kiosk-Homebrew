#include "video_path.h"

#include <coreinit/filesystem.h>
#include <nn/acp/client.h>
#include <nn/acp/result.h>
#include <nn/acp/title.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static bool
append_meta_video(int index, char *out, size_t outSize)
{
   char metaDir[FS_MAX_PATH];

   ACPInitialize();
   bool ok = ACPGetTitleMetaDir(ABOUT_WIIU_TID, metaDir, sizeof(metaDir)) == ACP_RESULT_SUCCESS;
   ACPFinalize();
   if (!ok) {
      return false;
   }

   snprintf(out, outSize, "%s/AboutWiiU%02d.mp4", metaDir, index);
   return true;
}

static bool
append_fallbacks(int index, char *out, size_t outSize)
{
   snprintf(out, outSize, "/vol/content/AboutWiiU%02d.mp4", index);
   return true;
}

bool
VideoPath_BuildIndex(int index, char *out, size_t outSize)
{
   if (!out || outSize == 0) {
      return false;
   }
   if (index < 0 || index >= ABOUT_WIIU_VIDEO_COUNT) {
      return false;
   }

   if (append_meta_video(index, out, outSize)) {
      return true;
   }

   return append_fallbacks(index, out, outSize);
}

static int
parse_index_arg(const char *arg)
{
   if (!arg || !*arg) {
      return -1;
   }

   char *end = NULL;
   long value = strtol(arg, &end, 10);
   if (end && *end == '\0' && value >= 0 && value < ABOUT_WIIU_VIDEO_COUNT) {
      return (int)value;
   }

   const char *prefix = "AboutWiiU";
   size_t prefixLen = strlen(prefix);
   if (strncmp(arg, prefix, prefixLen) != 0) {
      return -1;
   }

   const char *digits = arg + prefixLen;
   value = strtol(digits, &end, 10);
   if (end && (*end == '\0' || strcmp(end, ".mp4") == 0) &&
       value >= 0 && value < ABOUT_WIIU_VIDEO_COUNT) {
      return (int)value;
   }

   return -1;
}

bool
VideoPath_FromArgv(int argc, char **argv, char *out, size_t outSize)
{
   int index = 0;

   if (argc >= 2) {
      index = parse_index_arg(argv[1]);
      if (index < 0) {
         return false;
      }
   }

   return VideoPath_BuildIndex(index, out, outSize);
}
