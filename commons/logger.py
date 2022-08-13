import logging
import datetime


class Logger:
    log_to_file = None
    log_enabled = None

    def log(self, msg, prnt=True, exit_now=False):
        if self.log_enabled:
            if exit_now:
                logging.error(msg)
            else:
                logging.info(msg)
        if prnt and self.log_to_file is not None:
            print("{}:{}".format(datetime.datetime.now().strftime("%Y-%m-%d-%I:%M:%S %p"), msg))
        if exit_now is True:
            print("In exit"+str(exit_now))
            exit(exit_now)
        return

    def __init__(self, log_enabled, log_to_file):
        self.log_enabled = log_enabled
        self.log_to_file = log_to_file
        if self.log_enabled:
            if log_to_file is not None:
                logging.basicConfig(filename=self.log_to_file, format='%(asctime)s:%(message)s',
                                datefmt='%Y-%m-%d-%I:%M:%S %p')
            else:
                logging.basicConfig(format='%(asctime)s:%(message)s',
                                             datefmt='%Y-%m-%d-%I:%M:%S %p')
            self.log("Logging Enabled: {}".format(self.log_enabled), False, -1)
        return


if __name__ == '__main__':
    logger = Logger(True, "test.log")
    logger.log("Test Message", False, False)