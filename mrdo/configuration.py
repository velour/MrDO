import json

class Configuration(object):
    DO_API_KEY = 'DO_API_KEY'
    IRC_PASSWD = 'IRC_PASSWORD'
    IRC_UNAME  = 'IRC_USER_NAME'
    IRC_BLESSD = 'IRC_BLESSED_USERS' ## those that can start / stop the server
    IRC_OPS    = 'IRC_OPS'           ## those that can bless, unbless users
    IRC_SERVER = 'IRC_SERVER'
    IRC_CHAN   = 'IRC_CHAN'
    IRC_PORT   = 'IRC_PORT'
    CONFIG_PATH= 'CONFIG_PATH'

    KEYS = [DO_API_KEY, IRC_PASSWD, IRC_UNAME, IRC_BLESSD, IRC_OPS, IRC_SERVER, IRC_CHAN, IRC_PORT, CONFIG_PATH ]

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
        to_ret.settings[Configuration.CONFIG_PATH] = path
        return to_ret

    def to_path(self, path):
        """
        Convert the object to json and then stow it at path
        Will clobber any existing configuration file living there
        """
        prev_path = self.settings[Configuration.CONFIG_PATH]
        self.settings[Configuration.CONFIG_PATH] = path
        if self._validate():
            f = open(path,'w')
            json.dump(self.settings, f, sort_keys=True, indent=4)
            f.close()
        else:
            self.settings[Configuration.CONFIG_PATH] = prev_path
            raise Exception("Can't convert invalid configuration to JSON.")

    def _validate(self):
        """
        Run a sanity check on the object to make sure it's worth saving
        """
        ret = True
        for key in Conifguration.KEYS:
            if not self.settings.has_key(key):
                print ("Missing %s" % key)
                ret = False
        return ret

    def _set_server(self, server):
        self.settings[Configuration.IRC_SERVER] = server

    def _set_chan(self, chan):
        self.settings[Configuration.IRC_CHAN] = chan

    def _set_port(self, port):
        self.settings[Configuration.IRC_PORT] = port

    def get_auth_level(self, user):
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
        if self.get_auth_level(issuer) == Configuration.OP:
            if to_add in self.settings[Configuration.IRC_BLESSD]:
                print to_add, "already a user. Not adding them."
            else:
                self.settings[Configuration.IRC_BLESSD].append(to_add)
                print issuer, "Successfully added", to_add
        else:
            print issuer, "lacks authority to add blessed users."

    def rem_user(self, issuer, to_rem):
        """
        Removes a name from the list of IRC_UNAME, those that can start / stop servers
        """
        if self.get_auth_level(issuer) == Configuration.OP:
            if to_rem in self.settings[Configuration.IRC_BLESSD]:
                self.settings[Configuration.IRC_BLESSD].remove(to_rem)
                print to_rem, "successfully removed from blessed users by", issuer
            else:
                print to_rem, "not a blessed user."
        else:
            print issuer, "lacks authority to remove blessed users"

    def op_user(self, issuer, to_add):
        """
        Gives ops to user, allowing them to add other users to the list of folks
        who can start and stop servers.
        """
        if self.get_auth_level(issuer) == Configuration.OP:
            if to_add in self.settings[Configuration.IRC_OPS]:
                print to_add, "already an op. Not adding them."
            else:
                self.settings[Configuration.IRC_OPS].append(to_add)
                print issuer, "Successfully added", to_add
        else:
            print issuer, "lacks authority to add ops."

    def unop_user(self, issuer, to_rem):
        """
        Removes ops from a user.
        Issuer needs to be op, the person to be removed also needs to have ops.
        """
        if self.get_auth_level(issuer) == Configuration.OP:
            if to_rem in self.settings[Configuration.IRC_OPS]:
                self.settings[Configuration.IRC_OPS].remove(to_rem)
                print to_rem, "successfully removed from ops", issuer
            else:
                print to_rem, "not an op."
        else:
            print issuer, "lacks authority to unop users"

    def set_do_api_key(self, issuer, key_string):
        """
        Adds a digital ocean API key to the assoc list of users -> api keys
        """
        ## structure of DO_API_KEYS is an assoc list, issuer -> API_KEY, one per
        if self.get_auth_level(issuer) == Configuration.OP:
            self.settings[Configuration.DO_API_KEY]= key_string
            print "Set Digital Ocean API key"
        else:
            print issuer, "can't set the key as they aren't an operator.."
