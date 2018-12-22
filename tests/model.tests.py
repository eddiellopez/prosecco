import sys, os, time

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import model

def main():
    # m = model.Model()
    # serial = m.getApps("")
    # print(serial)

    testAppData()


def testAppData():
    appData = model.AppData()
    # load an empty prototype file
    os.popen("rm test_data.json")
    time.sleep(1)
    os.popen("cp test_data.json.empty test_data.json")
    time.sleep(1)
    
    appData.load("test_data.json")
    # Add a couple
    appData.add("My App", "/test/myApp.exe", "img.png")
    appData.add("My App", "/test/myOtherApp.exe", "img.png")
    appData.add("My App", "/test/myExtraOtherApp.exe", "img.png")
    # Save in another file
    appData.save("test_data_result.json")

    # Open an read
    appData.load("test_data_result.json")
    assert appData.count() == 3, "Wrong size!"

    appData.remove("/test/myApp.exe")
    assert appData.count() == 2, "Wrong size!"

    appData.save("test_data_result_two.json")
    assert appData.getJson == '{"programs": [{"name": "My App", "image": "img.png", "path": "/test/myOtherApp.exe"}, {"name": "My App", "image": "img.png", "path": "/test/myExtraOtherApp.exe"}]}' , "Wrong serialization!"
    print(appData.getJson())

if __name__ == "__main__":
    main()
