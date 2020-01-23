#!python

import os
import sys

import rarfile
from watchdog.events import FileSystemEventHandler

def log(msg):
    print(f'{msg}\n')
    #sys.stdout.write(msg)
    #sys.stdout.flush()

class Handler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()
        self.tracker = []
    

    #@staticmethod
    def on_any_event(self, event):
        log(f'{self.tracker}')
        sync_file = False
        rar_file = None

        if event.event_type == 'deleted':
            return None
        elif event.is_directory is True:
            if event.event_type == 'created' or event.event_type == 'modified':
                curr_dir = event.src_path
                
                try:
                    for file in os.listdir(curr_dir):
                        if file.endswith('.rar'):
                            log(f'RAR file found! [{file}]')
                            rar_file = file
                        if file.startswith('.syncthing'):
                            log(f'Sync file located in [{curr_dir}]')
                            sync_file = True
                            rar_file = None
                            break
                except FileNotFoundError as e:
                    log(f'Error deteched: [{e}')

                if sync_file == False and rar_file is not None:
                    if curr_dir not in self.tracker:
                        self.tracker.append(curr_dir)
                        log(f'Added [{curr_dir}] to tracker.')
                        rar = rarfile.RarFile(f'/{curr_dir}/{rar_file}')
                        try:
                            log(f'Extracting [{rar_file}]')
                            rar.extractall(path=curr_dir)
                        except rarfile.Error as e:
                            log(f'An error has occured with the extraction - {e}')
                            return None
                        rar_list = rar.namelist()
                        log(f'Cleaning up [{curr_dir}]')
                        for f in os.listdir(curr_dir):
                            if f not in rar_list:
                                os.remove(f'{curr_dir}/{f}')
                                log(f'[{curr_dir}/{f}] deleted.')
                        rar_file = None
                        self.tracker.remove(curr_dir)
                        log(f'Removed [{curr_dir}] from tracker.')
