import logging
import sys


class Config:
    MAIN_URL = 'https://www.imdb.com'
    TOP_250_URL = 'https://www.imdb.com/chart/top?ref_=nv_mv_250'
    HREF_LOCATION_IDX = 1
    TITLE_DELIMITER = '('
    TITLE_IDX = 0
    DIRECTOR_FIRST_IDX = 3
    DIRECTOR_SECOND_IDX = 0
    BATCH = 10
    TITLE_ZIP_IDX = 0
    DIRECTOR_ZIP_IDX = 1

    @classmethod
    def start_logging(cls):
        cls.logger = logging.getLogger('movies')
        cls.logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter("'%(asctime)s - %(threadName)s - %(name)s - %(levelname)s - %(message)s'")

        # create a file handler and add it to logger
        file_handler = logging.FileHandler('movies.log')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        cls.logger.addHandler(file_handler)

        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(logging.INFO)
        stream_handler.setFormatter(formatter)
        cls.logger.addHandler(stream_handler)
