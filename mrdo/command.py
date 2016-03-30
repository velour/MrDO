from configuration import Configuration

class Command(object):
    def __init__(self, keyword, shortDesc, longDesc, auth=Configuration.OP):
        self.auth = auth
        self.keyword = keyword
        self.shortDesc = shortDesc
        self.longDesc = longDesc

    def canIssue(self, config, issuer):
        """
        Can the command be issued by the user in questin according to the config
        """
        return config.get_auth_level(issuer) >= self.auth

    def __str__(self):
        return self.keyword

## Commands
help = Command("help",
               "Get help using the bot.",
               """List all commands the bot can accept, or ask for
               help on a specific command see detailed information
               along with a usage string.""",
               auth = Configuration.NO_ONE)

# User Management
op_user = Command("give_ops",
                  "Promote user to OP.",
                  """ Promotes a single user to operator status.
                  Operators can give other users the ability to start
                  and stop droplets or games (bless), and can start
                  and stop droplets and games themselves.""")

unop_user = Command("take_ops",
                    "Remove user from OP list.",
                    """ Removes a user from the list of
                    operators. Revokes their ability to promote users
                    to operator or blessed status..  If they are not
                    seperately users, this also removes their ability
                    to start and stop droplets and games.""")
add_user = Command("add_user",
                   "Add user to the list of users.",
                   """Users can start and stop droplets and games.""")
rem_user = Command("rem_user",
                   """Removes user privledges from a user.  This
                   revokes their ability to start and stop droplets
                   and games, so long as that user is not also an
                   operator.""")

# Droplet Manipulation
add_api_key = None
stop_droplet = None
list_images = None
load_most_recent_image = None
load_named_image = None
running_droplet = None

# Game Server Management
list_inits = None
list_ongoing = None
start_server = None
backup_server = None
stop_server = None

