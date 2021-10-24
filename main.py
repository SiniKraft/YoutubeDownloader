import sys
from qtapp import run


run(sys.argv[1].split("nickloryoutubedl://")[-1][:-1])
