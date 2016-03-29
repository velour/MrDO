import json

class Configuration(object):
    DO_API_KEY = 'DO_API_KEY'
    IRC_PASSWD = 'IRC_PASSWORD'
    IRC_UNAME  = 'IRC_USER_NAME'
    IRC_BLESSD = 'IRC_BLESSED_USERS' ## those that can start / stop the server
    IRC_OPS    = 'IRC_OPS' ## those that can bless, unbless users

    NO_ONE = 0
    BLESSED = 1
    OP = 2
    
    def __init__(self,settings):
        """
        Create an object representing the configuration of MrDo
        """
        self.settings = settings

    @staticmethod
    def from_path(path):
        """
        Create an object representing the configuration of MrDo from a json object
        """
        f = open(path, 'r')
        settingsDict = json.load(f)
        f.close()
        to_ret = Configuration(settingsDict)
        if not to_ret._validate():
            raise Exception("Error loading configuration from " + path + ": invalid settings.")
        return to_ret

    def to_path(self, path):
        """
        Convert the object to json and then stow it at path
        Will clobber any existing configuration file living there
        """
        if self._validate():
            f = open(path,'w')
            json.dump(self.settings, f, sort_keys=True, indent=4)
            f.close()
        else:
            raise Exception("Can't convert invalid configuration to JSON.")

    def _validate(self):
        """
        Run a sanity check on the object to make sure it's worth saving
        """
        ret = True

        if not self.settings.has_key(Configuration.DO_API_KEY):
            print "No Digital Ocean API Key"
            ret = False
        if not self.settings.has_key(Configuration.IRC_PASSWD):
            print "No IRC Password for Mr. Do"
            ret = False
        if not self.settings.has_key(Configuration.IRC_UNAME):
            print "No User Name for Mr. Do"
            ret = False
        if not self.settings.has_key(Configuration.IRC_BLESSD):
            print "No list of users for Mr. Do"
            ret = False
        if not self.settings.has_key(Configuration.IRC_OPS):
            print "No operators for Mr. Do"
            ret = False

        return ret

    def _get_auth_level(self, user):
        """
        Returns the authorization level of the user
        """
        if user in self.settings[Configuration.IRC_OPS]:
            return Configuration.OP
        elif user in self.settings[Configuration.IRC_BLESSD]:
            return Configuration.BLESSED
        else:
            return Configuration.NO_ONE

    def add_user(self, issuer, to_add):
        """
        Adds a user to the list of IRC_UNAME users, those that can start / stop servers
        """
        raise Exception("Stub: add_user")

    def rem_user(self, issuer, to_add):
        """
        Removes a name from the list of IRC_UNAME, those that can start / stop servers
        """
        raise Exception("Stub: rem_user")

    def bless_user(self, issuer, to_bless):
        """
        Blesses a user, allowing them to add other users to the list of folks
        who can start and stop servers.

        The issuer needs to be blessed, and the user being blessed needs to be
        authorized at the user level themselves
        """
        raise Exception("Stub: bless_user")

    def curse_user(self, issuer, to_curse):
        """
        Unblesses a user, moving them from blessed to user status.
        Issuer needs to be blessed, the person to be removed also
        needs to be blessed.
        """
        raise Exception("Stub: curse_user")

    def add_do_api_key(self, issuer, key_string):
        """
        Adds a digital ocean API key to the assoc list of users -> api keys
        """
        raise Exception("Stub: add_api_key")
