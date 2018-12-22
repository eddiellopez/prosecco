import subprocess

class Wine():
    def __init__(self):
        None
    
    def version():
        os.open("wine --version")

    def regeditExport(self, filename, key):
        subprocess.run(["wine", "regedit", "/E", filename, key])

