import json, os, logging 
import filewatcher, filesystemprocessor
import wine, registry, installer
from PySide2.QtCore import QObject, Slot, SLOT, SIGNAL

class Model(QObject):
    # TODO: Find path to C: dynamically
    DRIVE_C = "/home/irena/.wine/drive_c"
    APP_DATA_JSON = "app_data.json" 

    def __init__(self):
        """Loads the known application data into memory"""
        QObject.__init__(self)
        self.__eventProcessor = filesystemprocessor.FileSystemProcessor()
        self.__eventProcessor.install.connect(self.onInstalled)
        self.__eventProcessor.uninstall.connect(self.onUninstalled)
        self.__eventProcessor.update.connect(self.onMoved)
        
        # TODO: This step should be followed by a scan to detect changes
        # That may have happened when the app is off
        self.__appData = AppData()
        self.__appData.load(self.APP_DATA_JSON)

    # @Signal(str, str, str)
    def install(path, name, image):
        pass
    
    def install(path):
        pass
    
    def update(path, newPath, name, image):
        pass
    
    def setRootObject(self, rootObject):
        """
        Sets the QML 'root object' which will provide a communication interface with that side.
        It provides the following interface:
            onInstall(path, name, image)  
            onUninstall(path)
            onUpdate(path, newPath, newName, newIcon)
            onDataUpdated(data)
        """
        self.__rootObject = rootObject
        
        self.__fileWatcher = filewatcher.FileWatcher(self.DRIVE_C, self)
        self.__fileWatcher.start(self.__eventProcessor)
        # Populate the UI right away
        self.__onDataUpdated(self.__appData.getJson())

    def shutdown(self):
        self.__appData.save(self.APP_DATA_JSON)
        self.__fileWatcher.shutdown()

    @Slot(result=str)
    def getApps(self, s):
        """Returns the current list of apps, as JSON"""
        return self.__appData.getJson() 
    
    @Slot(str, result=str)
    def getTestApps(self, s):
        logging.info("Using TEST app JSON.")
        apps = []
        with open("apps.txt", "r") as f:
            for line in f:
                apps.append(line)
        r = "".join(apps)
        # logging.info("Returning: " + r)
        return r
    
    @Slot(str, result=bool)
    def openNew(self, path):
        if path:
            # Path may come with file:// scheme
            inst = installer.Installer(self.__onInstall)
            inst.install(path)
        else:
            logging.info("Empty path.")
        logging.info("openNew(): returning.")

    @Slot(result=bool)
    def uninstaller(self):
        os.popen("wine uninstaller")    
        
    @Slot(str, str)
    def onCardClicked(self, path, name):       
        os.popen(f"wine '{path}'")
    
    def __onInstall(self, path, name, image):
        logging.info("onInstallComplete() called; what: " + path)
        # TODO: Update in root object
        self.__rootObject.onInstall(path, name, image) 

    # Proxies for root object methods
    def __onUninstall(self, path):
        self.__rootObject.onUninstall(path)

    def __onUpdate(self, path, newPath, newName, newIcon):
        self.__rootObject.onUpdate(path, newPath, newName, newIcon)

    def __onDataUpdated(self, data):
        self.__rootObject.onDataUpdated(data)
    
    def __processDisplayIcon(self, imageUri):
        # TODO: Implement this
        logging.info("Warining: __processDisplayIcon() returning blank!")
        return ""
    
    @Slot(str, str, str)
    def onInstalled(self, path, name, icon):
        # Update model JSON with new app
        # Call __onInstall to just update the new element into the UI
        if self.__appData.add(path, name, icon):
            self.__appData.save(self.APP_DATA_JSON)
            self.__onInstall(path, name, icon)
    
    @Slot(str)
    def onUninstalled(self, path):
        # Update model JSON removing uninstalled app
        # Add a Call self.rootObject.onUninstallComplete(what)
        if self.__appData.remove(path):
            self.__appData.save(self.APP_DATA_JSON)
            self.__onUninstall(path)

    @Slot(str, str)
    def onMoved(self, path, new_path):
        # Update model JSON. 
        # Add a Call self.rootObject.onUpdateComplete(...)
        self.__appData.update(path, newPath=new_path)
        self.__appData.save(self.APP_DATA_JSON)
        # TODO: Check None at the Javascript side
        sel.__onUpdate(path, new_path, None, None)

class AppData():
    """
    Holds the applications data in memory. 
    Note the unique identifier for an application will be the installation path.

    __data is a map as: {"programs": [app, app, app]}
    # app is a map as: {"name": name, "image": img, "path": path}
    """
    def __init__(self):
        self.__data = None

    def load(self, filename):
        with open(filename, "r") as f:
            self.__data = json.load(f)

    def save(self, filename):
        with open(filename, "w") as f:
            json.dump(self.__data, f)

    def add(self, path, name, icon):
        """
        Check if already exists, otherwise elements could be repeated
        Returns True if the element was added, False if already exists.
        """
        lis = self.__data["programs"]
        for p in lis:
            if p["path"] == path:
                p["name"] = name
                p["image"] = icon
                return False
        # Just add the applications list
        self.__data["programs"].append({"name": name, "image": icon, "path": path})
        return True

    def remove(self, path):
        """
        Removes an element from the data.
        Returns true if the element was removed, False otherwise.
        """
        lis = self.__data["programs"] 
        for i, e in enumerate(lis):
            if e["path"] == path:
                del lis[i]
                return True
        return False

    def update(self, path, newName=None, newPath=None, newIcon=None):
        for e in self.__data["programs"]:
            if e["path"] == path:
                if newName:
                    e["name"] = newName
                if newPath:
                    e["path"] = newPath
                if newIcon:
                    e["image"] = newIcon
                break
        else:
            self.add(path, newName, newIcon)

    def count(self):
        return len(self.__data["programs"])
    
    def getJson(self):
        return json.dumps(self.__data)
