from config import log_file
from config import file_logging_level
from config import stream_logging_level
from config import logging_sdtout
from config import logging_file
from config import logging_format

import logging

def get_logger(name: str=__name__, flevel=file_logging_level, slevel=stream_logging_level, stdout: bool=logging_sdtout, fout: bool=logging_file, format: str=logging_format):
    '''
    logger object
    Params:
    name: str or logging object, stdout: bool and format str
    '''
    # Setting name for logger
    logger = logging.getLogger(name)
    fhandler = logging.FileHandler(log_file)
    shandler = logging.StreamHandler()

    # set the logger formater and the file output handler
    formatter = logging.Formatter(logging_format)
    shandler.setFormatter(formatter)
    fhandler.setFormatter(formatter)
    shandler.setLevel(slevel)
    fhandler.setLevel(flevel)

    # add the handler to logger
    if stdout: logger.addHandler(shandler)
    if fout: logger.addHandler(fhandler)
    return logger
def set_level(logger,level: str = "INFO"):
    '''
    set the level of a logger
    '''
    bypass = False
    if isinstance(level, int) : bypass = True
    if level == "debug" or bypass == True: logger.setLevel(logging.DEBUG)
    if level == "info" or bypass == True: logger.setLevel(logging.INFO)
    if level == "warning" or bypass == True : logger.setLevel(logging.WARNING)
    if level == "ERROR" or bypass == True : logger.setLevel(logging.ERROR)
    if level == "critical" or bypass == True : logger.setLevel(logging.CRITICAL)
    return logger