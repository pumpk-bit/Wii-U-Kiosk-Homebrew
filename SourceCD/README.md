# SourceCD (local only)

This folder is gitignored except this README. Put Nintendo dumps, original RPX/RPL files, boot screens, and Ghidra projects here so they never get committed.

Layout is up to you. A typical split:

```text
SourceCD/
  README.md          (this file)
  dumps/             extracted title folders
  ghidra/            .gpr projects and exported C
```

The homebrew apps in this repo are new code. They do not need anything from SourceCD to build.
