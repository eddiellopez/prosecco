import QtQuick 2.3
import QtQuick.Controls 2.4
import QtQuick.Window 2.2
import QtQuick.Layouts 1.11
import QtQuick.Dialogs 1.0
import "logic.js" as Logic

ApplicationWindow {
    id:appWindow

    property int cardWidth: 450
    property int cardHeight: 50
    property int margin: 5
    property int columns: 2
    property var cardList: []

    /**
     * Called by 'model' when an installation has been completed.
     * path is the path or ID of the element
     * what is what's knonw of the installed element.
     * what is what's knonw of the installed element.
     */
    function onInstall(path, name, image) {
        console.log("onInstall(): path=" + path + "; name=" + name + "; image=" + image)
        Logic.addObject(cardWidth, cardHeight, layout, name, image, path, onClickHandler, cardList)
    }

    /**
     * Called by 'model' when an installation has been completed.
     * path is the path or ID of the element
     */
    function onUninstall(path) {
        console.log("onUninstall(): path=" + path)
        Logic.remove(path, cardList);
    }

    /**
     * Called by 'model' when an update has happened.
     * path is the path or ID of the element
     * newPath is the new path to set, undefined/null (TODO: check) if not required
     * newName is the new name, undefined/null if none
     * newIcon is the new icon, undefined/null if none
     */
    function onUpdate(path, newPath, newName, newIcon) {
        console.log("onUpdate(): path=" + path + "; newPath=" + newPath + "; newIcon=" + newIcon)
        // TODO: Find and update
    }

    /**
     * Called by 'model' when new applications data is available.
     * data is delivered as a JSON, see logic.js for further details on the processing of this.
     */
    function onDataUpdated(json) {
        console.log("updateData(): " + json);
        Logic.addPrograms(cardWidth, cardHeight, layout, json, onClickHandler, cardList)
    }

    function initializeApps() {
        // var apps = model.getTestApps("edd")
        // Logic.addPrograms(lay, apps, onClickHandler);
    }

    function onClickHandler(name, appPath) {
        console.log("Clicked: " + name + ", path: " + appPath);
        model.onCardClicked(appPath, name);
    }

    function open() {
        fileDialog.open()
    }
    
    // Opens the wine uninstaller
    function uninstaller() {
        model.uninstaller()
    }

    // Starts the Open/Install process
    function install(path) {
        model.openNew(path)
    }

    title: qsTr("Prosecco")
    width: cardWidth * columns + (columns + 1) * margin // 2 (450px) columns + (5px) * 3 margins
    height: 480
    visible: true
    
    menuBar: MenuBar {
          Menu {
            title: qsTr("&File")
            Action { 
                text: qsTr("&Open...") 
                onTriggered: open()
            }
            Action { 
                text: qsTr("&Uninstaller") 
                onTriggered: uninstaller()
            }
            MenuSeparator { }
            Action { 
                text: qsTr("&Quit")
                onTriggered: Qt.quit()
            }
        }
    }
    
    GridLayout {
        id: layout
        anchors { left: parent.left; top: parent.top; leftMargin: margin; topMargin: margin}
        columns: appWindow.columns
    }
    
    FileDialog {
        id: fileDialog
        title: qsTr("Please choose a file")
        folder: shortcuts.home
        nameFilters: [ "Application files (*.exe *.msi)" ]
        onAccepted: {
            // Install what was selected
            install(fileDialog.fileUrl) 
            console.log("You chose: " + fileDialog.fileUrl)
        }
        onRejected: {
            console.log("Canceled")
        }
    }
    
    BusyIndicator {
        running: false
    }

    Component.onCompleted: {
        console.log("Ready.")
        initializeApps()
    }
}
