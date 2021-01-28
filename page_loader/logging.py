import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

debug_handler = logging.FileHandler(filename='./logging_debug.log', mode='w')
debug_handler.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)

debug_formatter = logging.Formatter(
            '%(asctime)s -%(name)s - %(levelname)s - %(message)s'
            )
stream_formatter = logging.Formatter('%(message)s')

debug_handler.setFormatter(debug_formatter)
stream_handler.setFormatter(stream_formatter)

logger.addHandler(debug_handler)
logger.addHandler(stream_handler)


