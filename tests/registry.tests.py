import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import registry


def test():
    reg = registry.Registry("file.reg")
    reg.printFullTree()
    entries = reg.get("Uninstall")
    print("returned entries: " + str(len(entries)))
    for e in entries:
        print("Key: " + e.name)
        n = e.get("DisplayName")
        # print(e.values)
        print("Display name is: " + str(n))

    reg2 = registry.Registry("missing.reg")
    reg2.printFullTree()

if __name__ == "__main__":
    test()
