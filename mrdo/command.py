from configuration import Configurationo

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
