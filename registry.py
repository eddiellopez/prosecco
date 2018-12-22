import re

class Registry():
    """Provides registry dump parsing features."""
    def __init__(self, filename):
        self.root = Entry("root")
        self.currentEntry = None
        self.currentKey = None
        self.__open(filename)

    def get(self, name) -> list:
        """
        Return a list of keys under the name.
        The key named 'name' itself will be returned also.
        """
        result = []
        # Do not return 'root' key
        for entry in self.root.getEntries():
            result.extend(self.__get(entry, name))
        return result

    def __get(self, entry, name):
        print("entry name: " + entry.name + ", name: " + name)
        if entry.name == name:
            res = [entry]
            res.extend(entry.getEntries())
            return res
        else:
            result = []
            for e in entry.getEntries():
                result.extend(self.__get(e, name))
        return result

    def __open(self, filename):
        """
        Opens a registre file dump, as produced by 'wine registry /e filename, key'
        and builds the depicted tree.
        """
        try:
            with open(filename, encoding="utf-16", errors='ignore') as f:
                for line in f:
                    isEntry, isValue, isContinueValue, info = self.__classify(line)
                    if isEntry:
                        self.__insert(self.root, info)
                        # print("Current Entry: " + str(self.currentEntry))
                    elif isValue:
                        self.__addValue(self.currentEntry, info)
                    elif isContinueValue:
                        self.__appendToValue(self.currentEntry, self.currentKey, info)
            return True #TODO October 23, 2018: Improve return codes
        except IOError as e:
            print(f"__open failed with: {e}")
            return False

    def __classify(self, line) -> tuple:
        """
        Classifies a registry file line in three possible categories:
        a) A new entry
        b) A value
        c) The continuation of the previously found falue

        The result will be delivered in a tuple, indicating which of the three a, b or c is
        true in the first three positions. The information will be in the fourth position.
        """
        match = re.search(r"\[(.+)\]", line)
        if match:
            # print("classify(): Entry found: " + match.group(1))
            return (len(match.group(1)) > 0, False, False, match.group(1))
        match = re.search(r"(.+=.+)", line)
        if match: 
            # print("classify(): Value found: " + match.group(1))
            return (False, len(match.group(1)) > 0, False, match.group(1))
        if self.__notBlank(line):
            # print("classify(): Continuation value found: " + line)
            return (False, False, True, line)
        return (False, False, False, None)

    def __insert(self, parent, line):
        """
        Inserts a new registry entry in the specified parent.
        This function will navigate down the tree hierarchy to insert at the correct position.
        Note that it strongly relies in the consistency provided by the 'wine registry' output.
        Updates the 'self.currentEntry' pointer.
        """
        # print("Insert(): " + line)
        if "\\" not in line:
            # print("Creating: " + line + ", adding it to: " + parent.name)
            entry = Entry(line.strip())
            parent.addEntry(entry)
            self.currentEntry = entry
        else:
            i = line.find("\\")
            parentPrefix = line[0:i].strip()
            # print("Prefix: " + parentPrefix)
            par = parent.getEntry(parentPrefix)
            if par is None:
                # print("Creating: " + parentPrefix + ", adding it to: " + parent.name)
                par = Entry(parentPrefix)
                parent.addEntry(par)
            else:
                pass
                # print(".Found.")
            self.__insert(par, line[i + 1:].strip())

    def __addValue(self, entry, line):
        """
        Adds a value to a registry entry. Note as of October 23, 2018 values are not 
        processed/fixed in any way and will go in its raw format.
        Updates the "self.currentKey' pointer.
        """
        if entry is None:
            # print("__addValue(): No entry to add: " + line)
            return None
        else:
            i = line.find("=")
            key, value = line[:i].strip("\""), line[i + 1:].strip("\"")
            # print(f"Adding: {key}:{value}")
            entry.add(key, value)
            self.currentKey = key

    def __appendToValue(self, entry, key, value):
        """Appends to a value mapped with key."""
        if entry and key:
            entry.add(key, value.strip("\""))

    def __notBlank(self, s):
        """Returns True if the argument is blank by not containing any word characters."""
        return re.search("\w+", s)

    def printFullTree(self):
        print("Registry Tree:")
        if self.root:
            self.printTree(self.root, 0)
        else:
            print("Empty")

    def printTree(self, entry, level):
        space = " " * level
        print(f"{space}+ {entry.name}")
        for key in entry.keys():
            print(f"{space} - {key}:{entry.get(key)}")
        for subEntry in entry.getEntries():
            self.printTree(subEntry, level + 1)


class Entry():
    """
    Represents an entry in the registry tree.
    Entries have a name, may have sub-entries and name-value pairs.
    """
    def __init__(self, name):
        self.name = name
        self.values = {}
        self.entries = {}

    def add(self, key, value):
        self.values[key] = value

    def keys(self):
        return self.values.keys()

    def get(self, key):
        return self.values.get(key)

    def addEntry(self, entry):
        self.entries[entry.name] = entry

    def getEntry(self, name):
        return self.entries.get(name)

    def getEntries(self):
        return self.entries.values()



