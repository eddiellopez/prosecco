var component;
var card;

/**
 * Adds a card to the contained.
 */
function addObject(width, height, containerId, name, imageUri, path, onClickHandler, list) {
    console.log("addObject(): name: " + name);
    component = Qt.createComponent("card.qml");
    card = component.createObject(containerId, {/*"width": x, "height": y*/});

    if (card == null) {
        // Error Handling
        console.log("Error creating object");
    }
    
    card.setName(name)
    card.setImageUri(imageUri)
    card.setAppPath(path)
    card.onClicked.connect(onClickHandler)

    // Add to list
    list.push(card)
}

function remove(path, list) {
    console.log("  List:")
    var pos = -1;
    list.forEach(function(item, index, array) {
        console.log(showProps(item, "QQuickRectangle_QML_156"))
        console.log(item.appPath)
        if (item.appPath == path) {
            pos = index;
        }
    });

    if (pos >= 0) {
        console.log("Destroying : " + path)
        var removedItem = list.splice(pos, 1); // this is how to remove an item
        removedItem.opacity = 0
        removedItem.destroy(1000)
    }
}

function showProps(obj, objName) {
  var result = '';
  for (var i in obj) {
    // obj.hasOwnProperty() is used to filter out properties from the object's prototype chain
    if (obj.hasOwnProperty(i)) {
      result += objName + '.' + i + ' = ' + obj[i] + '\n';
    }
  }
  return result;
}

/**
 * Adds all the programs as cards from its serialized form.
 * Format:
 *   { 
 *      "programs": [
 *      {
 *        "name": "LinkedIn",
 *        "image": "li.png",
 *        "path": "/home/LinkedIn"
 *      },
 *      {
 *        "name": "Stack Overflow",
 *        "image": "so.png",
 *        "path": "/home/Stack Overflew"
 *      },...
 *   }
 */
function addPrograms(width, height, containerId, appsJson, onClickHandler, list) {
    var obj = JSON.parse(appsJson);
    var apps = obj.programs;
    
    for (var i = 0; i < apps.length; i++) {
        addObject(width, height, containerId, apps[i].name, apps[i].image, apps[i].path, onClickHandler, list);
    }
}

