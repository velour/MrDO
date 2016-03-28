import datettime

def saveWorld(Object):
    INITIAL_WORLD = 0 ## Starting world state, for things like factorio speedrun
    ONGOING_PLAY = 1
    ARCHIVED = 2 ## Saved game state not meant to be saved over, just
                 ## Loaded up for display.

    def __init__(name=None, path=None, shortDesc = None, longDesc = None,
                 createdDate = None, state = ONGOING_PLAY):
        self.name = name
        self.path = path
        self.shortDesc = shortDesc
        self.longDesc = longDesc
        if createdDate:
            self.createdDate = createdDate
        else:
            self.createdDate = datetime.datetime.utcnow()
        self.state = state

    def str_of_type(t):
        if t == INITIAL_WORLD:
            return "Initial World"
        elif t == ONGOING_PLAY:
            return "Active"
        elif t == ARCHIVED:
            return "Archived"
        else:
            raise Exception("unrecognized world state: " + str(t))

    def __str__(self):
        retString = "[%s] %s" % (str_of_type self.state, self.name)
        return retSrting

    def copy(self):
        raise Exception("Stub of copy")

    def remove(self):
        raais Exception("Stub of remove")

    def toJSON(self, outpath=None):
        """
        Renders the non-code portions of the savedWorld object to json for
        transmission and storage.

        Raises an exception if the object is missing fields when we try
        to reduce it to json.
        """
        saveDict = {}
        saveDict['name'] = self.name
        saveDict['path'] = self.path
        saveDict['shortDesc'] = self.shortDesc
        saveDict['longDesc'] = self.longDesc
        saveDict['createdDate'] = self.createdDate
        saveDict['state'] = self.state

        for (id, obj) in saveDict.items():
            if obj == None:
                exString = "saveWorld missing field %s; aborting save." % id
                raise Exception(exString)

        if outpath:
            ## here we marshall the object to disk
            raise Exception("print json to stdout stub")
        else:
            raise Exception("flush json to disk stub")

    def fromJSON(saveDict):
        """
        Construct a saved world object from a JSON description of it's relevant
        fields.
        """
        return savedWorld(name = saveDict['name'],
                          path = saveDict['path'],
                          shortDesc = saveDict['shortDesc'],
                          longDesc = saveDict['longDesc'],
                          createdDate = saveDict['createdDate'],
                          state = saveDict['state'])

    def fromPath(p):
        """
        Construct a saved world object from a path painting at a json file that
        describes it.
        """
        raise Exception("Stub of fromPath")
        jsonOfPath = None ## fill in with loading json from path
        return fromJSON(jsonOfPath)
