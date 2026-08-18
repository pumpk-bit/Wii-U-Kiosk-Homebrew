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

#define KIOSK_FEATURED_LIST_TID 0x000500001FA82200ull

static const char *
name_for_title(uint64_t titleId)
{
   switch (titleId) {
   case 0x000500021FA82201ull: return "our featured demo";
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
   WHBLogPrintf("Loaded %d featured titles from %s", out->count, path);
   return true;
}

static bool
load_featured_list(FSClient *client, FSCmdBlock *cmd, FeaturedList *out)
{
   char path[FS_MAX_PATH];
   char metaDir[FS_MAX_PATH];

   ACPInitialize();

   /* How the kiosk menu finds this catalog: meta of title 000500001FA82200. */
   if (ACPGetTitleMetaDir(KIOSK_FEATURED_LIST_TID, metaDir, sizeof(metaDir)) == ACP_RESULT_SUCCESS) {
      snprintf(path, sizeof(path), "%s/Featured.xml", metaDir);
      if (try_load(client, cmd, path, out)) {
         ACPFinalize();
         return true;
      }
   }

   /* Same lookup for whatever title we were launched as (WUP install / Aroma). */
   uint64_t self = OSGetTitleID();
   if (self != KIOSK_FEATURED_LIST_TID) {
      if (ACPGetTitleMetaDir(self, metaDir, sizeof(metaDir)) == ACP_RESULT_SUCCESS) {
         snprintf(path, sizeof(path), "%s/Featured.xml", metaDir);
         if (try_load(client, cmd, path, out)) {
            ACPFinalize();
            return true;
         }
      }
   }

   ACPFinalize();

   /* WUHB / packaged content. */
   if (try_load(client, cmd, "/vol/content/Featured.xml", out)) {
      return true;
   }

   if (WHBMountSdCard()) {
      snprintf(path, sizeof(path), "%s/wiiu/apps/featured_list/Featured.xml",
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
print_featured_list(const FeaturedList *list)
{
   WHBLogPrintf("Featured list (%s) — show these titles:", list->type);
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

   WHBLogPrintf("Featured List  (00050000-1FA82200)");
   WHBLogPrintf("Catalog for the kiosk featured row.");
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
      if (load_featured_list(client, cmd, &list)) {
         print_featured_list(&list);
      } else {
         WHBLogPrintf("No Featured.xml found.");
         WHBLogPrintf("Install this title as 000500001FA82200,");
         WHBLogPrintf("or place Featured.xml in /vol/content/");
         WHBLogPrintf("or sd:/wiiu/apps/featured_list/");
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
