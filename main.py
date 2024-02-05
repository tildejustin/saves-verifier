#!/usr/bin/env python

import argparse
import json
import os
from pathlib import Path

from save import WorldSave

version = "1.0.0"
verbose = False


def is_save_folder(path: str) -> Path:
    if (os.path.isdir(path) and os.path.exists(os.path.join(path, "level.dat"))) or (os.path.isfile(path) and path.endswith(".json")):
        return Path(path)
    else:
        raise argparse.ArgumentTypeError(f"{path} does not contain a level.dat file")


def main():
    global verbose
    parser = argparse.ArgumentParser(
        prog="Save Verifier",
        description="Verifies save files for MCSR",
        epilog="By tildejustin, based off of SavesFolderReader by DuncanRuns"
    )
    parser.add_argument("save_folder", metavar="F", nargs="+", type=is_save_folder, default=os.curdir, help="the folder(s) to check")
    parser.add_argument("-l", "--log", )
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s {version}")
    parser.add_argument("-ver", "--verbose", action="store_true")
    parser.add_argument("-a", "--advancements", action="store_true", help="prints the number of advancements. if -v it also prints the names. takes an advancements file.")
    args = parser.parse_args()
    verbose = args.verbose
    advancements_only = args.advancements

    for save_folder in args.save_folder:
        if advancements_only:
            with open(save_folder) as f:
                print(len(list(filter(lambda s: not s.startswith("minecraft:recipe"), json.load(f)))))
            continue
        save = WorldSave(save_folder)
        text = str(save)
        print(text)


if __name__ == "__main__":
    main()
