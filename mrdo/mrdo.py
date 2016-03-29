## Jordan Thayer  2016-03-21T14:21:37-04:00
## A stump simple IRC client for managing servers on a digital ocean instance

import irc.client
import irc.modes
from irc.dict import IRCDict
from irc.bot import SingleServerIRCBot, ServerSpec

default_server = ServerSpec("someIrcServer", password = "notthepassword")

class MrDo(SingleServerIRCBot):

    def __init__(self, server=default_server):
        SingleServerIRCBot.__init__(self,[server], "MrDo", "MrDo")
        self.operators = ["some", "secret", "powerful", "people"]
        self.channel = "#aChannelToConnectTo"

    def on_welcome(self,c,e):
        c.join(self.channel)

    def on_dccchat(self,c,e):
        print c, e

    def on_privmsg(self,c,e):
        print "got private message", e.arguments[0]

    def on_pubmsg(self,c,e):
        a = e.arguments[0].split(':', 1)
        if len(a) > 1 and irc.strings.lower(a[0]) == irc.strings.lower("MrDo"):
            print "got command", a[1].strip()
