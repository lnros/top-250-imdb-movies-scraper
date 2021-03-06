
from conf import Config as cfg
from imdbScraper import IMDBScraper


def main():
    """
    It compares the time of getting, parsing, and printing the top 250 movies list of titles and directors from IMDB
    by doing so one at a time or in batches.
    """

    cfg.start_logging()
    cfg.logger.info("Scraping list of top 250 movies")
    imdb = IMDBScraper()
    cfg.logger.info("Getting the 250 different urls")
    urls = imdb.get_250_info()
    imdb.scrape_one_by_one(urls)
    cfg.logger.info("Finished one by one")
    imdb.scrape_in_batches(urls)
    cfg.logger.info("Finished in batches")


if __name__ == '__main__':
    main()
