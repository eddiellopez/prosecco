import QtQuick 2.0
import QtGraphicalEffects 1.0

Rectangle {
    id: papa
    property string appPath
    property int m: 5
    property color primary: "#90a4ae"  
    property color primaryLight: "#c1d5e0"  
    property color primaryDark: "#62757f"  

    signal onClicked(string name, string path)

    function setName(text) {
        title.text = text;
    }

    function setImageUri(imageUri) {
        image.source = imageUri;
    }

    function setAppPath(path) {
        appPath = path
    }

    function destroy(delay) {
        papa.destroy(delay)
    }

    color: primary 
    radius: 5 
    width: 450
    height: 50
    antialiasing: true
    layer.enabled: true
    layer.effect: DropShadow {
                transparentBorder: true
                radius: 8
                samples: 17
                horizontalOffset: 3
                verticalOffset: 3
    }

    Image {
        id: image
        anchors { 
            left: parent.left; top: parent.top; bottom: parent.bottom; 
            leftMargin: parent.m; topMargin: parent.m; bottomMargin: parent.m 
        }
        width: parent.height - 10
        sourceSize.width: 1024
        sourceSize.height: 1024
    }

    Text {
        id: title
        anchors.left: image.right
        anchors.leftMargin: 5
        anchors.verticalCenter :parent.verticalCenter
        // Wrap text?
        width: parent.width
        wrapMode: Text.WordWrap
    }

    MouseArea {
        anchors.fill: parent
        hoverEnabled: true
        onClicked: {
            parent.onClicked(title.text, parent.appPath)
        }

        onEntered: {
            parent.color = parent.primaryDark
        }

        onExited: {
            parent.color = parent.primary
        }
    }
}
