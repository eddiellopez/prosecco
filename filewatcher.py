import sys, time
import pathlib
from watchdog.observers import Observer

class FileWatcher():

    def __init__(self, directory, appListener):
        self.__observer = Observer()
        self.__directory = directory
        self.__appListener = appListener

    def start(self, eventHandler):
        self.__observer.schedule(eventHandler, self.__directory, recursive = True)
        self.__observer.start()
    
    def shutdown(self):
        self.__observer.stop()
        self.__observer.join()

