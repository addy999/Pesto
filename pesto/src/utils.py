import sys
import os
import time
import logging
import glob
from typing import List

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

BLOB = "**/*test*.py"
FILE_BLOBS = ["**/*_test.py", "**/test_*.py", "**/test.py"]


def match_dir(dir: str) -> List[str]:
    return glob.glob(dir + BLOB, recursive=True)


def match_file(file_path: str) -> bool:
    return True in [
        glob.fnmatch.fnmatch(file_path, FILE_BLOB) for FILE_BLOB in FILE_BLOBS
    ]


def format_error_msg(msg: list) -> str:

    """
    Sample:
    Traceback (most recent call last):
        File "/home/addy/Documents/PEst/pesto/../pesto/classes.py", line 17, in run
            self.func()
        File "/home/addy/Documents/PEst/demo/function_test.py", line 12, in test_awesome_function_cases
            expect(my_awesome_function(1, 1)).to_be(3.5)
        File "/home/addy/Documents/PEst/pesto/../pesto/expect.py", line 14, in to_be
            assert self.val == a, str(self.val) + " does not equal " + str(a)
    AssertionError: 35.5 does not equal 3.5
    """

    phrases_to_skip = ["Traceback", "pesto", "assert " "self."]
    lines_to_keep = []
    for line in msg:
        to_keep = True
        # line = line.strip()
        for phrase in phrases_to_skip:
            if phrase in line:
                to_keep = False
                break
        if to_keep:
            lines_to_keep.append(line)

    return "\n".join(lines_to_keep[1:])


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


def start_watcher(tester, dir_path: str) -> None:
    observer = Observer()
    observer.schedule(RestartTestHandler(tester), dir_path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()
