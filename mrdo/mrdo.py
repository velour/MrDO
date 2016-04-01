## Jordan Thayer  2016-03-21T14:21:37-04:00
## A stump simple IRC client for managing servers on a digital ocean instance

import irc.client
import irc.modes
import digitalocean
import dropletManager
from irc.dict import IRCDict
from irc.bot import SingleServerIRCBot, ServerSpec
from configuration import Configuration

# Basic commands
from command import helpCmd, running_droplet
# User management commands
from command import op_user, unop_user, add_user, rem_user
# Droplet management commands
from command import add_api_key, stop_droplet, list_images, load_most_recent_image, load_named_image
# a list of all commands
from command import commands


default_config = Configuration.from_path("./default_config.json")

def serverOfConfig(config):
    return ServerSpec(config.settings[Configuration.IRC_SERVER],
                      port=config.settings[Configuration.IRC_PORT],
                      password=config.settings[Configuration.IRC_PASSWD])

class MrDo(SingleServerIRCBot):

    def __init__(self, config):
        SingleServerIRCBot.__init__(self,
                                    [serverOfConfig(config)],
                                    config.settings[Configuration.IRC_UNAME],
                                    config.settings[Configuration.IRC_UNAME])
        self.config = config
        self.channel = config.settings[Configuration.IRC_CHAN]
        self.droplet = None
        self.manager = None
        if self.config.settings[Configuration.DO_API_KEY]:
            try:
                key = self.config.settings[Configuration.DO_API_KEY]
                if key:
                    self.manager = digitalocean.Manager(token=key.strip())
            except:
                print "Couldn't setup a digital ocean manager. Key is bogus?"

    def on_welcome(self,c,e):
        c.join(self.channel)

    def on_dccchat(self,c,e):
        print c, e

    def on_privmsg(self,c,e):
        user = e.source.nick
        command = e.arguments[0]
        command = command.split(' ')
        self._handle_msg(user, user, command)

    def on_pubmsg(self,c,e):
        a = e.arguments[0].split(':', 1)
        if len(a) > 1 and irc.strings.lower(a[0]) == irc.strings.lower(self.config.settings[Configuration.IRC_UNAME]):
            cmd = a[1].strip()
            user = e.source.nick
            chan = e.target
            cmd = cmd.split(' ')
            self._handle_msg(chan, user,cmd)

    def _respond(self, chan, message):
        """
        Prints the given message to the given channel
        """
        self.connection.notice(chan, message)

    def _insufficient_privledge(self, user, cmd):
        """
        Tells the user privately that they lack privledges to run the issued command
        """
        response = "%s lacked privledges to issue %s" % (user, cmd)
        self._respond(user, response)

    def _helpCmd(self, rc, user, cmd):
        """
        Runs the helpCmd command.  If it's just helpCmd, print short
        description of all commands, otherwise print the long
        description of the supplied commands.
        """
        cmd = cmd[1:]
        print cmd
        if cmd == []:
            ## print short description of every command
            for c in commands:
                self._respond(rc, ("%s: %s" % (c.keyword, c.shortDesc)))
        else:
            for c in cmd:
                self._respond(rc, ("%s: %s" % (c.keyword, c.longDesc)))

    def _running_droplet(self, rc, user, cmd):
        """
        Respond with some simple information about the running droplet.  It's name,
        how long it's been running, which image it was spawned from.
        """
        if self.droplet:
            pass
        else:
            self._respond(rc, "There is no running droplet.")

    def _op_user(self, rc, user, cmd):
        """
        Promote the user to Operator
        """
        ## User has already been authenticated.
        cmd = cmd[1:]
        ret_string = "Gave ops to"
        for uname in cmd:
            self.config.op_user(user, uname)
            ret_string = "%s %s" % (ret_string, uname)
        self._respond(rc, ret_string)

    def _unop_user(self, rc, user, cmd):
        """
        Revoke a user's operator privledges
        """
        cmd = cmd[1:]
        ret_string = "Removed ops from"
        for uname in cmd:
            self.config.unop_user(user, uname)
            ret_string = "%s %s" % (ret_string, uname)
        self._report(rc, ret_string)

    def _add_user(self, rc, user, cmd):
        """
        Bless a user as being able to start, stop droplets
        """
        cmd = cmd[1:]
        ret_string = "Blessed"
        for uname in cmd:
            self.config.add_user(user, uname)
            ret_string = "%s %s" % (ret_string, uname)
        self._respond(rc, ret_string)

    def _rem_user(self, rc, user, cmd):
        """
        Remove a user's droplet starting, stopping privledges
        """
        cmd = cmd[1:]
        ret_string = "Cursed"
        for uname in cmd:
            self.config.rem_user(user, uname)
            ret_string = "%s %s" % (ret_string, uname)
        self._respond(rc, ret_string)

    def _add_api_key(self, rc, user, cmd):
        """
        Associate a Digital Ocean API key with a given user
        """
        key = cmd[1]
        print key
        try:
            self.manager = digitalocean.Manager(token=key.strip())
            print "manager set"
            self.config.set_do_api_key(user, key)
            print "key set"
            self._respond(rc, "Set Digital Ocean key")
        except:
            self._respond(rc, "Failed to set Digital Ocean key")

    def _stop_droplet(self, rc, user, cmd):
        """
        Stop a droplet, save it's image
        """
        name = None
        try:
            name = cmd[1]
        except:
            pass
        if self.manager:
            if self.droplet:
                self._respond(rc, "Tearing down the droplet, this may take a while.")
                dropletManager.tearDown(self.manager, self.droplet, name=name)
                self._respond(rc, "The droplet has been destroyed.")
            else:
                self._respond(rc, "No droplet to tear down.")
        else:
            self._respond(rc, "No manager to handle droplets.")

    def _list_images(self, rc, user, cmd):
        """
        list all images associated with the issuer's API key
        """
        if self.manager:
            images = self.manager.get_my_images()
            imageList = ""
            for image in images:
                imageList = "%s %s" % (imageList, image.name)
            self._respond(rc, imageList)
        else:
            self._respond(rc, "No manager / api key.  Can't list images.")

    def _load_most_recent_image(self, rc, user, cmd):
        """
        load the most recent image associated with the issuer's API key as a droplet
        """
        if self.manager:
            if self.droplet == None:
                try:
                    image = dropletManager.get_most_recent_image(self.manager)
                    self._respond(rc, ("Starting droplet of %s" % image.name))
                    self.droplet = dropletManager.droplet_of_image(image, self.manager)
                    self._respond(rc, "Droplet started.")
                except:
                    self._respond(rc, "Failed to start the droplet for some reason.")
            else:
                self._respond(rc, "There's a droplet running. Not starting a new one.")
        else:
            self._respond(rc, "No manager / api key.  Can't load an image.")

    def _load_named_image(self, rc, user, cmd):
        """
        Start the named image as a new droplet
        """
        if self.manager:
            if self.droplet == None:
                try:
                    self._respond(rc, ("Trying to start %s" % cmd[1]))
                    image = dropletManager.get_image_by_name(self.manager, cmd[1])
                    self._respond(rc, ("Starting droplet of %s" % image.name))
                    self.droplet = dropletManager.droplet_of_image(image, self.manager)
                    self._respond(rc, "Droplet started.")
                except:
                    self._respond(rc, "Failed to start the droplet for some reason.")
            else:
                self._respond(rc, "There's a droplet running. Not starting a new one.")
        else:
            self._respond(rc, "No manager / api key.  Can't load an image.")


    def _handle_msg(self, response_chan, user, cmd):
        """
        Dispatches the appropriate command
        """
        print user, "issued", cmd
        if cmd == []:
            return
        cmd_name = cmd[0]
        if cmd_name == helpCmd.keyword:
            if helpCmd.canIssue(self.config, user):
                self._helpCmd(response_chan, user, cmd)
            else:
                self._insufficient_privledge(user, cmd)
        elif cmd_name == running_droplet.keyword:
            if running_droplet.canIssue(self.config, user):
                self._running_droplet(response_chan, user, cmd)
            else:
                self._insufficient_privledge(user, cmd)
        elif cmd_name == op_user.keyword:
            if op_user.canIssue(self.config, user):
                self._op_user(response_chan, user, cmd)
            else:
                self._insufficient_privledge(user, cmd)
        elif cmd_name == unop_user.keyword:
            if unop_user.canIssue(self.config, user):
                self._unop_user(response_chan, user, cmd)
            else:
                self._insufficient_privledge(user, cmd)
        elif cmd_name == add_user.keyword:
            if add_user.canIssue(self.config, user):
                self._add_user(response_chan, user, cmd)
            else:
                self._insufficient_privledge(user, cmd)
        elif cmd_name == rem_user.keyword:
            if rem_user.canIssue(self.config, user):
                self._rem_user(response_chan, user, cmd)
            else:
                self._insufficient_privledge(user, cmd)
        elif cmd_name == add_api_key.keyword:
            if add_api_key.canIssue(self.config, user):
                self._add_api_key(response_chan, user, cmd)
            else:
                self._insufficient_privledge(user, cmd)
        elif cmd_name == stop_droplet.keyword:
            if stop_droplet.canIssue(self.config, user):
                self._stop_droplet(response_chan, user, cmd)
            else:
                self._insufficient_privledge(user, cmd)
        elif cmd_name == list_images.keyword:
            if list_images.canIssue(self.config, user):
                self._list_images(response_chan, user, cmd)
            else:
                self._insufficient_privledge(user, cmd)
        elif cmd_name == load_most_recent_image.keyword:
            if load_most_recent_image.canIssue(self.config, user):
                self._load_most_recent_image(response_chan, user, cmd)
            else:
                self._insufficient_privledge(user, cmd)
        elif cmd_name == load_named_image.keyword:
            if load_named_image.canIssue(self.config, user):
                self._load_named_image(response_chan, user, cmd)
            else:
                self._insufficient_privledge(user, cmd)
        else: ## No recognized keyword
            self._respond(user, "I don't recognize that command. Try issuing 'help'.")
