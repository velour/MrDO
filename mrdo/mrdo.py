## Jordan Thayer  2016-03-21T14:21:37-04:00
## A stump simple IRC client for managing servers on a digital ocean instance

import irc.client
import irc.modes
from irc.dict import IRCDict
from irc.bot import SingleServerIRCBot, ServerSpec
from configuration import Configuration

# Basic commands
from command import help, running_droplet
# User management commands
from command import op_user, unop_user, add_user, rem_user
# Droplet management commands
from command import add_api_key, stop_droplet, list_images, load_most_recent_image, load_named_image
# a list of all commands
from command import commands


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

    def on_welcome(self,c,e):
        c.join(self.channel)

    def on_dccchat(self,c,e):
        print c, e

    def on_privmsg(self,c,e):
        user = e.source.nick
        command = e.arguments[0]
        command = command.split(' ', 1)
        self._handle_msg(user, user, command)

    def on_pubmsg(self,c,e):
        a = e.arguments[0].split(':', 1)
        if len(a) > 1 and irc.strings.lower(a[0]) == irc.strings.lower(self.config.settings[Configuration.IRC_UNAME]):
            cmd = a[1].strip()
            user = e.source.nick
            chan = e.target
            cmd = cmd.split(' ', 1)
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
        response = "%s lacked privledges to issue %s", % (user, cmd)
        self._respond(user, response)

    def _help(self, rc, user, cmd):
        """
        Runs the help command.  If it's just help, print short
        description of all commands, otherwise print the long
        description of the supplied commands.
        """
        pass

    def _running_droplet(self, rc, user, cmd):
        """
        Respond with some simple information about the running droplet.  It's name,
        how long it's been running, which image it was spawned from.
        """
        pass

    def _op_user(self, rc, user, cmd):
        """
        Promote the user to Operator
        """
        pass

    def _unop_user(self, rc, user, cmd):
        """
        Revoke a user's operator privledges
        """
        pass

    def _add_user(self, rc, user, cmd):
        """
        Bless a user as being able to start, stop droplets
        """
        pass

    def _rem_user(self, rc, user, cmd):
        """
        Remove a user's droplet starting, stopping privledges
        """
        pass

    def _add_api_key(self, rc, user, cmd):
        """
        Associate a Digital Ocean API key with a given user
        """
        pass

    def _stop_droplet(self, rc, user, cmd):
        """
        Stop a droplet, save it's image
        """
        pass

    def _list_images(self, rc, user, cmd):
        """
        list all images associated with the issuer's API key
        """
        pass

    def _load_most_recent_image(self, rc, user, cmd):
        """
        load the most recent image associated with the issuer's API key as a droplet
        """
        pass

    def _load_named_image(self, rc, user, cmd):
        """
        Start the named image as a new droplet
        """
        pass

    def _handle_msg(self, response_chan, user, cmd):
        """
        Dispatches the appropriate command
        """
        print user, "issued", cmd
        if cmd == []:
            return
        cmd_name = cmd[0]
        cmd = None
        if cmd_name == help.keyword:
            if help.canIssue(user, self.config):
                self._help(response_chan,cmd)
            else:
                self._insufficient_privledge(user, cmd)
        elif cmd_name == running_droplet.keyword:
            if running_droplet.canIssue(user, self.config):
                pass
            else:
                self._insufficient_privledge(user, cmd)
        elif cmd_name == op_user.keyword:
            if op_user.canIssue(user, self.config):
                pass
            else:
                self._insufficient_privledge(user, cmd)
        elif cmd_name == unop_user.keyword:
            if unop_user.canIssue(user, self.config):
                pass
            else:
                self._insufficient_privledge(user, cmd)
        elif cmd_name == add_user.keyword:
            if add_user.canIssue(user, self.config):
                pass
            else:
                self._insufficient_privledge(user, cmd)
        elif cmd_name == rem_user.keyword:
            if rem_user.canIssue(user, self.config):
                pass
            else:
                self._insufficient_privledge(user, cmd)
        elif cmd_name == add_api_key.keyword:
            if add_api_key.canIssue(user, self.config):
                pass
            else:
                self._insufficient_privledge(user, cmd)
        elif cmd_name == stop_droplet.keyword:
            if stop_droplet.canIssue(user, self.config):
                pass
            else:
                self._insufficient_privledge(user, cmd)
        elif cmd_name == list_images.keyword:
            if list_images.canIssue(user, self.config):
                pass
            else:
                self._insufficient_privledge(user, cmd)
        elif cmd_name == load_most_recent_image.keyword:
            if load_most_recent_image.canIssue(user, self.config):
                pass
            else:
                self._insufficient_privledge(user, cmd)
        elif cmd_name == load_named_image.keyword:
            if load_named_image.canIssue(user, self.config):
                pass
            else:
                self._insufficient_privledge(user, cmd)
        else: ## No recognized keyword
            self._respond(user, "I don't recognize that command. Try issuing 'help'.")
