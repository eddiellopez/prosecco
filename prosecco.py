#!/usr/bin/env python3

import os
import sys
import json
from PySide2.QtCore import QUrl, QObject, Slot
from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine
import model

def main():
    sys.argv += ['--style', 'material']
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    _model = model.Model()

    context = engine.rootContext()
    context.setContextProperty("model", _model)

    qmlFile = os.path.join(os.path.dirname(__file__), 'view.qml')
    engine.load(QUrl.fromLocalFile(os.path.abspath(qmlFile)))
    
    if not engine.rootObjects():
        sys.exit(-1)
        
    roots = engine.rootObjects()
   
    # The 'rootObject' in 'view.qml' provides the following top level functions:
    # onInstallComplete(what)
    _model.setRootObject(roots[0])

    res = app.exec_()
    # Deleting the view before it goes out of scope is required to make sure all child QML instances
    # are destroyed in the correct order.
    del engine
    sys.exit(res)


if __name__ == '__main__':
    main()

