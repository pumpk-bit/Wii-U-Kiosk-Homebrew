#include <coreinit/title.h>
#include <whb/log.h>
#include <whb/log_cafe.h>
#include <whb/log_console.h>
#include <whb/proc.h>

/*
 * Kiosk Menu never launches this RPX for Exhibition Mode playback.
 * MenuApp reads /meta/TVnn.mp4 and /meta/DRCnn.mp4 from this title directly
 * when nonInteractiveMode is enabled. This binary exists only so the title
 * installs cleanly on MLC.
 */
int
main(int argc, char **argv)
{
   WHBProcInit();
   WHBLogCafeInit();
   WHBLogConsoleInit();

   WHBLogPrintf("Exhibition Mode  (00050000-1FA82700)");
   WHBLogPrintf("Title ID %016llX", (unsigned long long)OSGetTitleID());
   WHBLogPrintf("This wrapper is not used by Kiosk Menu in Exhibition Mode.");
   WHBLogPrintf("Install TVnn.mp4 + DRCnn.mp4 under meta/ on this title.");

   for (int i = 0; i < argc; ++i) {
      WHBLogPrintf("argv[%d] = %s", i, argv[i]);
   }

   WHBLogConsoleDraw();
   while (WHBProcIsRunning()) {
      WHBLogConsoleDraw();
   }

   WHBLogConsoleFree();
   WHBLogCafeDeinit();
   WHBProcShutdown();
   return 0;
}
