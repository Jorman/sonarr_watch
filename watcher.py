#!python

import time
from watchdog.observers import Observer

import handler

class Watcher:
    def __init__(self, dir):
        self.watch_directory = dir
        self.observer = Observer()
        print(f'Watching [{self.watch_directory}]\n')

    def run(self):
        event_handler = handler.Handler()
        self.observer.schedule(event_handler,
                              self.watch_directory,
                              recursive=True)

        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("\nERROR: Stopping watcher.\n")
            
        self.observer.join()
