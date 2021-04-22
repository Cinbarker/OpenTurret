import logging

# Set default logging format. Import CustomExceptions to set this format
logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s] %(levelname)-8s: %(message)-50s  [%(lineno)d %(name)s]",
    datefmt='%H:%M:%S')


class InvalidCallsignError(Exception):
    pass
