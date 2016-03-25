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
