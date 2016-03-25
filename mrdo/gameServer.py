import datetime

def game(Object):
    RUNNING = 1
    NOT_RUNNING = 0

    def __init__(name=None, password = None, started = None):
        self.name = Name
        self.password = password
        self.started = started
        self.server_pid = None
        self.status = NOT_RUNNING

    def __str__(self):
        return self.name

    def uptime (self):
        """
        Tell me how long the server has been up.
        Return a time suitable for printing
        """
        raise Exception("stub")

    def is_running(self):
        """
        Tell me if the server is currently active
        Return a boolean
        """
        self.update_status()
        return self.status == RUNNING

    def halt(self):
        """
        Gracelessly kill the server
        """
        raise Exception("stub")

    def update_status(self):
        """
        Use the proc file system or similar to updated the status of the server.
        Basically, go check if the process is still alive or not.
        """
        if self.server_pid:
            raise Exception("stub -- need to see pid is active")
        else:
            self.status = NOT_RUNNING
        return self.status

    def list_worlds(self):
        """
        Return a list of initial worlds the server has to choose from
        """
        raise Exception("stub")
