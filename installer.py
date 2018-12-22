import os
import urllib.parse
from PySide2.QtCore import QProcess, Slot

class Installer():
    """Provides basic installing features"""
    def __init__(self, onInstallCompleteListener):
        self._onInstallCompleteListener = onInstallCompleteListener 
    
    def install(self, path):
        """Installs the prgram using wine"""
        print("Installing: " + path)
        uri = urllib.parse.urlparse(path)
        qprocess = QProcess()
        qprocess.finished.connect(self.onFinished)
        qprocess.errorOccurred.connect(self.onErrorOccurred)
        qprocess.setProgram("wine")
        qprocess.setArguments(["".join(uri[1:])])
        # qprocess.start() # This Crashes
        qprocess.startDetached() # This does not supports signals
        
        # os.popen("wine " + "'" + files + "'")
        # try:
            # completedProcess = subprocess.run(["wine", f"{files}"], check=True)
            # remove file:// schemme            
        # with ThreadPoolExecutor(max_workers=4) as executor:
        #    executor.submit(self.poll, path, onInstallCompleteListener)

    def onFinished(self, exitCode, exitStatus):
        print("Finished!!!!!")
        self._onInstallCompleteListener("use path here!") 

    def onErrorOccurred(self, error):
        print(error)

    def poll(self, path, onInstallCompleteListener):
        uri = urllib.parse.urlparse(path)
        with subprocess.Popen(["wine", "".join(uri[1:])]) as proc:
            # outs, errs = proc.communicate()
            pass
        onInstallComplete(files)

