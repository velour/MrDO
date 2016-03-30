from configuration import Configuration

class Command(object):
    def __init__(self, keyword, shortDesc, longDesc, usage, auth=Configuration.OP):
        self.auth = auth
        self.keyword = keyword
        self.shortDesc = shortDesc
        self.longDesc = longDesc
        self.usage = usage

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
               ["help", "help <command>"],
               auth = Configuration.NO_ONE)

# User Management
op_user = Command("give_ops",
                  "Promote user to OP.",
                  """ Promotes a single user to operator status.
                  Operators can give other users the ability to start
                  and stop droplets or games (bless), and can start
                  and stop droplets and games themselves.""",
                  ["give_ops <user>"]
                  )

unop_user = Command("take_ops",
                    "Remove user from OP list.",
                    """ Removes a user from the list of
                    operators. Revokes their ability to promote users
                    to operator or blessed status..  If they are not
                    seperately users, this also removes their ability
                    to start and stop droplets and games.""",
                    ["take_ops <user>"]
                    )
add_user = Command("add_user",
                   "Add user to the list of users.",
                   """Users can start and stop droplets and games.""",
                   ["add_user <user>"]
                   )
rem_user = Command("rem_user",
                   "Removes user from list of users.",
                   """Removes user privledges from a user.  This
                   revokes their ability to start and stop droplets
                   and games, so long as that user is not also an
                   operator.""",
                   ["rem_user <user>"]
                   )

# Droplet Manipulation
add_api_key = Command("add_key",
                      "Associates a Digital Ocean API Key with a user name.",
                      """All droplet tasks require an API key to
                      accomplish.  The key is used to authenticate the
                      user for a digital ocean account or team.
                      Authentication lets us list and start
                      droplets.""",
                      ["add_key <string>, best done in a private message."],
                      auth = Configuration.BLESSED)
stop_droplet = Command("stop_droplet",
                       "Cleanly shut down the droplet.",
                       """Powers off the droplet, takes an image of
                       the machine's state, and saves that image to
                       the Digital Ocean account.  The droplet is then
                       destroyed to save money.  The whole process can
                       take around 15 minutes.""",
                       ["stop_droplet", "stop_droplet <image name>"],
                       auth = Configuration.BLESSED)

list_images = Command("list_images",
                      "List all Digital Ocean images",
                      """Lists all of the Digital Ocean images
                      associated with the user's API key.  These are
                      exactly the images that will be considered as
                      valid targets when attempting to load up an
                      image.""",
                      ["list_images"],
                      auth = Configuration.BLESSED)
load_most_recent_image = None
load_named_image = None
running_droplet = None

# Game Server Management
### Not going to flesh these out for a bit, since I've not started
### Writing this portion of Mr. Do
list_inits = None
list_ongoing = None
start_server = None
backup_server = None
stop_server = None
