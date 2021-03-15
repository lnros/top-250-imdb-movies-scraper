import time

import grequests
import requests
from bs4 import BeautifulSoup

from conf import Config as cfg


class IMDBScraper:
    """
    Given the IMDB's top 250 movies, this class gets and parses their titles and directors
    scrape_one_by_one does it one movie at a time, while scrape_in_batches scrapes a batch whose size is set in conf.py.
    """

    def __init__(self):
        r = requests.get(cfg.TOP_250_URL).text
        soup = BeautifulSoup(r, 'lxml')
        self._top250 = soup.find_all('td', class_='titleColumn')
        if not self._top250:
            cfg.logger.error(f'Empty top 250 list: {self._top250}')
        else:
            cfg.logger.debug(f"Size of top250: {len(self._top250)}")

    def get_250_info(self):
        """
        Retrieves the url for each one of the 250 top IMDB movies
        """
        cfg.logger.info("Getting Top 250 urls")
        urls = []
        for i, elem in enumerate(self._top250):
            url = elem.contents[cfg.HREF_LOCATION_IDX]['href']
            cfg.logger.debug(f"{i + 1}. Found the URL: {url}")
            urls.append(url)
        return urls

    @staticmethod
    def _parse_title_director(r):
        """
        Given a url request, it retrieves the movie's title and director
        """
        cfg.logger.info("Parsing title and director.")
        soup = BeautifulSoup(r.text, 'lxml')
        title_elem = soup.find('meta', property="og:title")
        if not title_elem:
            cfg.logger.error("Title not found")
        title = title_elem.attrs['content'].split(cfg.TITLE_DELIMITER)[cfg.TITLE_IDX]
        cfg.logger.debug(f"Title found: {title}")
        director_elem = soup.find('div', class_="credit_summary_item")
        if not director_elem:
            cfg.logger.error("Director not found")
        director = director_elem.contents[cfg.DIRECTOR_FIRST_IDX].contents[cfg.DIRECTOR_SECOND_IDX]
        cfg.logger.debug(f"Director found: {director}")
        return title, director

    def _get_title_director(self, url):
        """
        Given an IMDB movie url, it retrieves the movie's title and director
        """
        cfg.logger.info(f"Scraping {url}")
        r = requests.get(url)
        if r is None:
            cfg.logger.critical("A webpage content was expected, got None instead.")
        return self._parse_title_director(r)


    @staticmethod
    def measure_time(func):
        def func_with_measure_time(*args, **kwargs):
            before_time = time.time()
            result = func(*args, **kwargs)
            time_took = time.time() - before_time
            print(f'It took {func.__name__} {int(time_took)} seconds to execute')
            return result
        return func_with_measure_time
    

    @measure_time
    def scrape_one_by_one(self, urls):
        """
        Given a list of IMDB's movies urls, it prints the movies' titles and directors.
        It does so one at a time.
        """
        cfg.logger.info("Starting one by one")
        for i, url in enumerate(urls):
            title, director = self._get_title_director(cfg.MAIN_URL + url)
            if title and director:
                cfg.logger.debug(f"Movie info: {i + 1} - {title} - {director}")
                cfg.logger.info("Successfully found movie info.")
                print(f"{i + 1} - {title}- {director}")
            else:
                cfg.logger.error(f"Movie number {i + 1} info not found")

    def _get_batch_title_director(self, batch):
        """
        Given an IMDB movies' urls list, it retrieves the movies' titles and directors
        """
        cfg.logger.info(f"Scraping batch")
        rs = (grequests.get(url) for url in batch)
        resp = grequests.map(rs)
        cfg.logger.debug(f"Size of resp: {len(resp)}")
        titles = []
        directors = []
        for i, r in enumerate(resp):
            if r is None:
                cfg.logger.critical("A webpage content was expected, got None instead.")
            title, director = self._parse_title_director(r)
            if title and director:
                cfg.logger.info("Parsed title and director successfully")
            cfg.logger.debug(f"{i + 1}/{len(batch)} - title: {title}, director: {director}")
            titles.append(title)
            directors.append(director)
        return titles, directors

    @measure_time
    def scrape_in_batches(self, urls):
        """
        Given a list of IMDB's movies urls, it prints the movies' titles and directors.
        It does so in batches, working in parallel threads by using grequests.
        """
        cfg.logger.info("Starting in batches")
        for i in range(0, len(urls), cfg.BATCH):
            batch = [cfg.MAIN_URL + url for url in urls[i:i + cfg.BATCH]]
            titles, directors = self._get_batch_title_director(batch)
            if titles and directors:
                cfg.logger.info(f"Batch retrieved successfully.")
                for j, movie_info in enumerate(zip(titles, directors)):
                    print(f"{j + i + 1} - {movie_info[cfg.TITLE_ZIP_IDX]}- {movie_info[cfg.DIRECTOR_ZIP_IDX]}")
            else:
                cfg.logger.error(f"Batch starting in index urls[{i}] went wrong.")
