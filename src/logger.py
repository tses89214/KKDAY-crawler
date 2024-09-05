import logging
import sys

def setup_logger():
    logger = logging.getLogger('crawler')
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        # File handler
        file_handler = logging.FileHandler('crawler.log')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger