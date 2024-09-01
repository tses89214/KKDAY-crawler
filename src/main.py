import time
from crawler import KKDAYCrawler
from logger import setup_logger

logger = setup_logger()

def main():
    logger.info("Starting KKDAY Crawler application")
    start_time = time.time()

    try:
        crawler = KKDAYCrawler()
        crawler.run()
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
    finally:
        end_time = time.time()
        duration = end_time - start_time
        logger.info(f"KKDAY Crawler application finished. Total runtime: {duration:.2f} seconds")

if __name__ == "__main__":
    main()
