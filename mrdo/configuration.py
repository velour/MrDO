import json

def Configuration(object):
    DO_API_KEY = 'DO_API_KEY'
    IRC_PASSWD = 'IRC_PASSWORD'
    IRC_UNAME  = 'IRC_USER_NAME'
    IRC_BLESSD = 'IRC_BLESSED_USERS' ## those that can start / stop the server
    IRC_OPS    = 'IRC_OPS' ## those that can bless, unbless users

    NO_ONE = 0
    USER = 1
    BLESSED = 2

    def __init__(settings):
        """
        Create an object representing the configuration of MrDo
        """
        self.settings = settings

    def from_json(json_obj):
        """
        Create an object representing the configuration of MrDo from a json object
        """
        raise Exception("stub: from_json")

    def _get_auth_level(self, user):
        """
        Returns the authorization level of the user
        """
        raise Exception("stub: _is_authorized")

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

    def to_json(self):
        """
        Convert the object to json for storage / transmission
        """
        raise Exception("Stub: to_json")

    def to_path(self, path):
        """
        Convert the object to json and then stow it at path
        """
        raise Exception("stub: to_path")

    def _validate(self):
        """
        Run a sanity check on the object to make sure it's worth saving
        """
        raise Exception("stub: validate")
