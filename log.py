from pathlib import Path


def parse_log(log: Path):
    with open(log) as l:
        for e in l:
            