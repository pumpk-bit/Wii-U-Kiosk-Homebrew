#include "featured.h"

#include <coreinit/filesystem.h>
#include <coreinit/memdefaultheap.h>
#include <coreinit/thread.h>
#include <coreinit/title.h>
#include <nn/acp/client.h>
#include <nn/acp/result.h>
#include <nn/acp/title.h>
#include <whb/log.h>
#include <whb/log_cafe.h>
#include <whb/log_console.h>
#include <whb/proc.h>
#include <whb/sdcard.h>

#include <stdio.h>
#include <string.h>

#define KIOSK_NEW_RELEASES_TID 0x000500001FA82300ull
#define CATALOG_XML "NewReleases.xml"

static const char *
name_for_title(uint64_t titleId)
{
   switch (titleId) {
   case 0x000500021FA82301ull: return "our new-releases demo";
   default:                   return "kiosk/eShop demo";
   }
}

static bool
try_load(FSClient *client, FSCmdBlock *cmd, const char *path, FeaturedList *out)
{
   WHBLogPrintf("Trying %s", path);
   if (!FeaturedList_LoadPath(client, cmd, path, out)) {
      return false;
   }
   WHBLogPrintf("Loaded %d titles from %s", out->count, path);
   return true;
}

static bool
load_catalog(FSClient *client, FSCmdBlock *cmd, FeaturedList *out)
{
   char path[FS_MAX_PATH];
   char metaDir[FS_MAX_PATH];

   ACPInitialize();

   if (ACPGetTitleMetaDir(KIOSK_NEW_RELEASES_TID, metaDir, sizeof(metaDir)) == ACP_RESULT_SUCCESS) {
      snprintf(path, sizeof(path), "%s/" CATALOG_XML, metaDir);
      if (try_load(client, cmd, path, out)) {
         ACPFinalize();
         return true;
      }
   }

   uint64_t self = OSGetTitleID();
   if (self != KIOSK_NEW_RELEASES_TID) {
      if (ACPGetTitleMetaDir(self, metaDir, sizeof(metaDir)) == ACP_RESULT_SUCCESS) {
         snprintf(path, sizeof(path), "%s/" CATALOG_XML, metaDir);
         if (try_load(client, cmd, path, out)) {
            ACPFinalize();
            return true;
         }
      }
   }

   ACPFinalize();

   snprintf(path, sizeof(path), "/vol/content/%s", CATALOG_XML);
   if (try_load(client, cmd, path, out)) {
      return true;
   }

   if (WHBMountSdCard()) {
      snprintf(path, sizeof(path), "%s/wiiu/apps/new_releases/" CATALOG_XML,
               WHBGetSdCardMountPath());
      bool ok = try_load(client, cmd, path, out);
      WHBUnmountSdCard();
      if (ok) {
         return true;
      }
   }

   return false;
}

static void
print_catalog(const FeaturedList *list)
{
   WHBLogPrintf("New releases list (%s):", list->type);
   for (int i = 0; i < list->count; ++i) {
      const FeaturedTitle *t = &list->titles[i];
      WHBLogPrintf("  %2d  %016llX  %s",
                   t->order,
                   (unsigned long long)t->titleId,
                   name_for_title(t->titleId));
      WHBLogPrintf("      %s .. %s", t->startDate, t->endDate);
   }
}

int
main(int argc, char **argv)
{
   (void)argc;
   (void)argv;

   WHBProcInit();
   WHBLogCafeInit();
   WHBLogConsoleInit();

   WHBLogPrintf("New Releases  (00050000-1FA82300)");
   WHBLogPrintf("Catalog for the kiosk new-releases row.");
   WHBLogPrintf("Launched as %016llX", (unsigned long long)OSGetTitleID());

   FSInit();
   FSClient *client = MEMAllocFromDefaultHeap(sizeof(FSClient));
   FSCmdBlock *cmd = MEMAllocFromDefaultHeap(sizeof(FSCmdBlock));
   if (!client || !cmd) {
      WHBLogPrintf("FS alloc failed");
   } else {
      FSAddClient(client, FS_ERROR_FLAG_ALL);
      FSInitCmdBlock(cmd);

      FeaturedList list;
      if (load_catalog(client, cmd, &list)) {
         print_catalog(&list);
      } else {
         WHBLogPrintf("No " CATALOG_XML " found.");
         WHBLogPrintf("Install this title as 000500001FA82300,");
         WHBLogPrintf("or place " CATALOG_XML " in /vol/content/");
         WHBLogPrintf("or sd:/wiiu/apps/new_releases/");
      }

      FSDelClient(client, FS_ERROR_FLAG_ALL);
   }

   if (cmd) {
      MEMFreeToDefaultHeap(cmd);
   }
   if (client) {
      MEMFreeToDefaultHeap(client);
   }

   WHBLogConsoleDraw();
   while (WHBProcIsRunning()) {
      WHBLogConsoleDraw();
      OSSleepTicks(OSMillisecondsToTicks(100));
   }

   WHBLogConsoleFree();
   WHBLogCafeDeinit();
   WHBProcShutdown();
   return 0;
}
