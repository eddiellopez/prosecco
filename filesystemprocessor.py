import pathlib, logging, subprocess
from watchdog.events import FileSystemEventHandler
from PySide2.QtCore import QObject, Signal, SIGNAL

class ApplicationListener():
    """Callback interface to deliver events"""
    def onInstalled(self, path, name,icon):
        pass

    def onUninstalled(self, path):
        pass

    def onMoved(self, path, newPath):
        pass

class FileSystemProcessor(FileSystemEventHandler, QObject):
    """Processes FileSystem changes"""
    install = Signal(str, str, str)
    uninstall = Signal(str)
    update = Signal(str, str)

    def __init__(self):
        QObject.__init__(self)

    # Callbacks from FileWatcher when filesystem is altered
    def on_created(self, event):
        if event.is_directory:
            pass
        else:
            self.processFileCreated(event.src_path)

    def on_deleted(self, event):
        if event.is_directory:
            pass
        else:
            self.processFileDeleted(event.src_path)

    def on_moved(self, event):
        if event.is_directory:
            pass
        else:
            self.processFileMoved(event.src_path, event.dest_path)
    
    def on_modified(self, event):
        if event.is_directory:
            pass
        else:
            # Note file modified will be treated as created
            self.processFileCreated(event.src_path)

    def processFileCreated(self, path):
        if path.lower().endswith(".exe"):
            # Filter out uninstallers and temp files:
            if self.filterPath(path):
                return
            logging.info(f"processFileCreated(): path={path}")
            uri = pathlib.PurePath(path)
            # TODO: Implement Icon Pocessing
            # Note the name of the program will be just the name of the enclosing directory
            # This can be complemented later on using the registry. As of now, just 
            # use the complete path as unique ID when needed
            self.install.emit(path, uri.parts[-2], self.getImagePath(path))

    def processFileDeleted(self, path):
        if path.lower().endswith(".exe"):
            logging.info(f"processFileDeleted(): path={path}")
            # self._appListener.onUninstalled(path)
            self.uninstall.emit(path)

    def processFileMoved(self, path, destPath):
        if path.lower().endswith(".exe"):
            logging.info(f"processFileMoved(): path={path}")
            # self._appListener.onMoved(path, destPath)
            self.update.emit(path, destPath)

    def getImagePath(self, path):
        # Build a directory for the extracte icons
        exe = pathlib.PurePath(path)
        outputDir = pathlib.Path("./images/" + exe.parts[-2])
        outputDir.mkdir(exist_ok=True)
        
        subprocess.run(["wrestool", "-x", f"--output={str(outputDir)}", "-t14", path])
        icons = list(outputDir.glob("*.ico"))
        icons.sort()
        logging.info("getImagePath() Found icons: " + str(len(icons)))

        img = str(icons[0])
        logging.info(f"getImagePath(): Returned image path={img}")
        return img
            
    def filterPath(self, path):
        """
        Filters out uninstallers and temp files.
        Returns True if the path should be filtered out, False otherwise"""
        ul = ["install", "unin", "uninst"]
        for s in ul:
            if s in path.lower():
                logging.info(f"filterPath(): Ignoring Uninstaller for path={path}")
                return True
        # Filter out Temp:
        if "/home/irena/.wine/drive_c/users/irena/Temp/" in path:
            logging.info(f"filterPath(): Ignoring Temp file for path={path}")
            return True
        return False
