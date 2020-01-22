#!python

import sys

import watcher

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("usage: sonarr-extract.py <watch_directory>\n")
    else:
        w = watcher.Watcher(str(sys.argv[1]))
        w.run()