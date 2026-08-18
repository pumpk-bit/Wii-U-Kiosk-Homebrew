#include "featured.h"

#include <coreinit/filesystem.h>
#include <coreinit/memdefaultheap.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>

static const char *
find_attr(const char *tag, const char *name)
{
   char key[64];
   snprintf(key, sizeof(key), "%s=\"", name);
   const char *p = strstr(tag, key);
   if (!p) {
      return NULL;
   }
   return p + strlen(key);
}

static int
copy_until(const char *src, char quote, char *dst, size_t dstSize)
{
   size_t n = 0;
   while (src[n] && src[n] != quote && n + 1 < dstSize) {
      dst[n] = src[n];
      n++;
   }
   dst[n] = '\0';
   return (int)n;
}

bool
FeaturedList_Parse(const char *xml, FeaturedList *out)
{
   memset(out, 0, sizeof(*out));
   strncpy(out->type, "featured", sizeof(out->type) - 1);

   const char *type = strstr(xml, "type=\"");
   if (type) {
      copy_until(type + 6, '"', out->type, sizeof(out->type));
   }

   const char *p = xml;
   while (out->count < FEATURED_MAX_TITLES) {
      const char *tag = strstr(p, "<title ");
      if (!tag) {
         break;
      }
      const char *end = strchr(tag, '>');
      if (!end) {
         break;
      }

      FeaturedTitle *t = &out->titles[out->count];
      const char *order = find_attr(tag, "order");
      const char *start = find_attr(tag, "start_date");
      const char *stop = find_attr(tag, "end_date");
      if (order) {
         t->order = atoi(order);
      }
      if (start) {
         copy_until(start, '"', t->startDate, sizeof(t->startDate));
      }
      if (stop) {
         copy_until(stop, '"', t->endDate, sizeof(t->endDate));
      }

      const char *idStart = end + 1;
      while (*idStart == ' ' || *idStart == '\n' || *idStart == '\t') {
         idStart++;
      }
      t->titleId = strtoull(idStart, NULL, 16);
      out->count++;
      p = end + 1;
   }

   return out->count > 0;
}

bool
FeaturedList_LoadPath(FSClient *client, FSCmdBlock *cmd, const char *path, FeaturedList *out)
{
   FSStat stat;
   if (FSGetStat(client, cmd, path, &stat, FS_ERROR_FLAG_ALL) != FS_STATUS_OK) {
      return false;
   }
   if (stat.size == 0 || stat.size > 64 * 1024) {
      return false;
   }

   FSFileHandle handle = 0;
   if (FSOpenFile(client, cmd, path, "r", &handle, FS_ERROR_FLAG_ALL) != FS_STATUS_OK) {
      return false;
   }

   char *buf = MEMAllocFromDefaultHeap(stat.size + 1);
   if (!buf) {
      FSCloseFile(client, cmd, handle, FS_ERROR_FLAG_ALL);
      return false;
   }

   FSStatus n = FSReadFile(client, cmd, (uint8_t *)buf, 1, stat.size, handle, 0, FS_ERROR_FLAG_ALL);
   FSCloseFile(client, cmd, handle, FS_ERROR_FLAG_ALL);
   if (n < 0) {
      MEMFreeToDefaultHeap(buf);
      return false;
   }

   buf[stat.size] = '\0';
   bool ok = FeaturedList_Parse(buf, out);
   MEMFreeToDefaultHeap(buf);
   return ok;
}
