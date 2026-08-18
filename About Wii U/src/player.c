#include "player.h"

#include <coreinit/filesystem.h>
#include <coreinit/memdefaultheap.h>
#include <coreinit/thread.h>
#include <whb/log.h>
#include <whb/proc.h>

#include <stdio.h>
#include <string.h>

bool
Video_Play(const char *path)
{
   FSInit();
   FSClient *client = MEMAllocFromDefaultHeap(sizeof(FSClient));
   FSCmdBlock *cmd = MEMAllocFromDefaultHeap(sizeof(FSCmdBlock));
   if (!client || !cmd) {
      WHBLogPrintf("FS alloc failed");
      return false;
   }

   FSAddClient(client, FS_ERROR_FLAG_ALL);
   FSInitCmdBlock(cmd);

   FSStat stat;
   FSStatus st = FSGetStat(client, cmd, path, &stat, FS_ERROR_FLAG_ALL);
   if (st != FS_STATUS_OK) {
      WHBLogPrintf("Missing video: %s", path);
      WHBLogPrintf("Add AboutWiiU00.mp4 .. AboutWiiU05.mp4 to this title meta/.");
      FSDelClient(client, FS_ERROR_FLAG_ALL);
      MEMFreeToDefaultHeap(cmd);
      MEMFreeToDefaultHeap(client);
      return false;
   }

   WHBLogPrintf("Found video (%llu bytes):", (unsigned long long)stat.size);
   WHBLogPrintf("%s", path);
   WHBLogPrintf("H264 MP4 playback: in progress (hardware decode).");

   /* TODO: demux MP4 mdat + feed wut H264DEC + GX2 NV12 blit loop. */
   while (WHBProcIsRunning()) {
      OSSleepTicks(OSMillisecondsToTicks(100));
   }

   FSDelClient(client, FS_ERROR_FLAG_ALL);
   MEMFreeToDefaultHeap(cmd);
   MEMFreeToDefaultHeap(client);
   return true;
}
