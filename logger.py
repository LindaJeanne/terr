from time import strftime, gmtime

DEFAULT_LOG_NAME = 'terrlog.txt'


class Logger(object):

    def __init__(self, filename=DEFAULT_LOG_NAME, log_level=3, set_echo=True):
        self.filename = filename
        self.log_level = log_level
        self.echo = set_echo

    def _write_to_log(self, msg, prefix=None, timestamp=True):
        the_time = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        with open(self.filename, 'a') as f:
            f.write(the_time + prefix + msg + "\n")
        if self.echo:
            print(the_time, prefix, msg)

    def log_error(self, msg):
        self._write_to_log(msg, ' [ERROR] ')

    def log_warning(self, msg):
        if self.log_level >= 1:
            self._write_to_log(msg, ' [WARNING] ')

    def log_info(self, msg):
        if self.log_level >= 2:
            self._write_to_log(msg, ' [INFO] ')

    def log_debug(self, msg):
        if self.log_level >= 3:
            self._write_to_log(msg, ' [DEBUG] ')
