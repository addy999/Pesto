import sys
import os
import time
import logging
import glob

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

BLOB = "**/*test*.py"


def match_dir(dir: str):
    return glob.glob(dir + BLOB, recursive=True)


def match_file(file_path: str):
    return glob.fnmatch.fnmatch(file_path, BLOB)


class RestartTestHandler(FileSystemEventHandler):
    def __init__(self, tester):
        super().__init__()

        self.tester = tester

    def on_modified(self, event):
        super().on_modified(event)

        if not event.is_directory:
            file_path = event.src_path
            if match_file(file_path):
                self.tester()


def start_watcher(tester, dir_path: str):
    observer = Observer()
    observer.schedule(RestartTestHandler(tester), dir_path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()
