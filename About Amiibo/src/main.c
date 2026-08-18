#include "player.h"
#include "video_path.h"

#include <coreinit/thread.h>
#include <coreinit/title.h>
#include <whb/log.h>
#include <whb/log_cafe.h>
#include <whb/log_console.h>
#include <whb/proc.h>

#include <stdio.h>

int
main(int argc, char **argv)
{
   char videoPath[512];

   WHBProcInit();
   WHBLogCafeInit();
   WHBLogConsoleInit();

   WHBLogPrintf("About Amiibo  (00050000-1FA83300)");
   WHBLogPrintf("Launched as %016llX", (unsigned long long)OSGetTitleID());

   for (int i = 0; i < argc; ++i) {
      WHBLogPrintf("argv[%d] = %s", i, argv[i]);
   }

   if (!VideoPath_FromArgv(argc, argv, videoPath, sizeof(videoPath))) {
      WHBLogPrintf("Could not resolve video path.");
      WHBLogPrintf("Expected argv[1] = 0 or AboutAmiibo00");
      WHBLogConsoleDraw();
      while (WHBProcIsRunning()) {
         WHBLogConsoleDraw();
         OSSleepTicks(OSMillisecondsToTicks(100));
      }
      WHBLogConsoleFree();
      WHBLogCafeDeinit();
      WHBProcShutdown();
      return 1;
   }

   WHBLogPrintf("Selected: %s", videoPath);
   WHBLogConsoleDraw();

   Video_Play(videoPath);

   WHBLogConsoleFree();
   WHBLogCafeDeinit();
   WHBProcShutdown();
   return 0;
}
