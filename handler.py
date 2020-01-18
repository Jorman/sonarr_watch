import os
import sys

import rarfile
from watchdog.events import FileSystemEventHandler

def log(msg):
        sys.stdout.write(msg)
        sys.stdout.flush()

class Handler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()
        self.tracker = []
    

    #@staticmethod
    def on_any_event(self, event):
        sync_file = False
        rar_file = None

        if event.event_type == 'deleted':
            return None
        elif event.is_directory is True:
            if event.event_type == 'created' or event.event_type == 'modified':
                curr_dir = event.src_path

                for file in os.listdir(curr_dir):
                    if file.endswith('.rar'):
                        rar_file = file
                    if file.startswith('.syncthing'):
                        log(f'Sync file located in {curr_dir}')
                        sync_file = True
                        rar_file = None
                        break

                if sync_file == False and rar_file is not None:
                    if curr_dir not in self.tracker:
                        self.tracker.append(curr_dir)
                        rar = rarfile.RarFile(f'/{curr_dir}/{rar_file}')
                        try:
                            log(f'Extracting {rar_file}\n')
                            rar.extractall(path=curr_dir)
                        except rarfile.Error as e:
                            log(f'An error has occured with the extraction - {e}')
                            return None
                        rar_list = rar.namelist()
                        log(f'Cleaning up {curr_dir}\n')
                        for f in os.listdir(curr_dir):
                            if f not in rar_list:
                                os.remove(f'{curr_dir}/{f}')
                        rar_file = None
                        self.tracker.remove(curr_dir)
