#!/usr/bin/python3

import sys

USAGE_HELP_MSG = """Usage:
\t$ python3 {0} x
where in/x is the input filepath and out/x is the output filepath"""

if len(sys.argv) != 2:
    print(USAGE_HELP_MSG.format(sys.argv[0]))
    exit(1)

filename = sys.argv[1].lower()

all_input = []
with open(f"in/{filename}", "r") as fin:
    all_input = fin.readlines()

print(all_input)

with open(f"out/{filename}", "w") as fout:
    fout.write("".join(all_input))
