---
title: Command reference
nav_order: 90
---

# Command reference

This page is generated from the code by `tools/gen_docs_reference.py`; do not edit it by hand.
The other pages explain each command step by step.

## `heat3d-wot-replay`

```text
usage: heat3d-wot-replay [-h] -o OUT [--force] [--version] replays [replays ...]

World of Tanks replays into 3DHeat tables

positional arguments:
  replays        .wotreplay files, or folders searched for them

options:
  -h, --help     show this help message and exit
  -o, --out OUT  folder to write into (a folder per map inside)
  --force        convert again what is already written
  --version      show program's version number and exit
```
