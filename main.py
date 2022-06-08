import os
import shutil
import time
import logging
from os.path import splitext, exists

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import date

source_dir = '/Users/eliasmansfield/Downloads/'
dest_dir_img = '/Users/eliasmansfield/Desktop/Billeder/'
dest_dir_vid = '/Users/eliasmansfield/Desktop/Videoer/'
dest_dir_zip = '/Users/eliasmansfield/Desktop/Zip/'
dest_dir_py = '/Users/eliasmansfield/Desktop/Python/'
dest_dir_exe = '/Users/eliasmansfield/Desktop/Programmer/'
dest_dir_doc = '/Users/eliasmansfield/Desktop/Documenter/'

img_ext = [".jpeg", ".jpg", ".png", ".gif", ".svg"]
vid_ext = [".mkv", ".flv", ".vob", ".ogv", ".mng", ".avi", ".mov", ".qt", ".wmv", ".yov",
           ".rm", ".asf", ".mp4", ".m4v", ".m4p", ".mpg", ".mpeg", ".m2v", ".m4v", ".svi",
           ".mxf", ".flv", ".f4v"]
zip_ext = [".zip"]
py_ext = [".py"]
exe_ext = [".dmg"]
doc_ext = [".doc", ".docx", ".odt", ".pdf", ".xls", ".xlsx", ".ppt", ".pptx"]

timevar = ["TIME", "__time__"]


def make_unique(path, destination):
    filename, extension = os.path.splitext(path)
    counter = 1
    # * IF FILE EXISTS, ADDS NUMBER TO THE END OF THE FILENAME
    while exists(f'{destination}{path}'):
        path = f"{filename} ({counter}){extension}"
        counter += 1
    return path


def move_file(extension, destination):
    with os.scandir(source_dir) as entries:
        for entry in entries:
            name = entry.name
            file_name, file_ext = os.path.splitext(entry)
            if file_ext in extension:
                if exists(f"{destination}{name}"):
                    unique_name = make_unique(name, destination)
                    os.rename(entry, f'{destination}{unique_name}')
                else:
                    shutil.move(entry.path, destination)


"""def move_file(dest, entry, name):
    if exists(f"{dest}/{name}"):
        unique_name = make_unique(name)
        os.rename(entry, unique_name)
    shutil.move(entry, dest)"""


class MoveHandler(FileSystemEventHandler):
    def on_modified(self, event):
        move_file(img_ext, dest_dir_img)
        move_file(vid_ext, dest_dir_vid)
        move_file(zip_ext, dest_dir_zip)
        move_file(py_ext, dest_dir_py)
        move_file(exe_ext, dest_dir_exe)
        move_file(doc_ext, dest_dir_doc)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = source_dir
    event_handler = MoveHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
