from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from driver import create_driver
from logger import setup_logger
from config_parser import config
import csv
import time

logger = setup_logger()

class KKDAYCrawler:
    def __init__(self):
        logger.info("Initializing KKDAYCrawler")
        self.driver = create_driver()
        self.config = config
        self.base_url = "https://www.kkday.com/zh-tw/city/"
        logger.info("KKDAYCrawler initialized successfully")
    
    def run(self):
        logger.info("Starting crawl process")
        all_products = []
        try:
            for city in self.config.get('cities', []):
                for currency in self.config.get('currencies', []):
                    products = self.crawl_city_currency(city, currency.upper())
                    all_products.extend(products)
                    time.sleep(5)
            
            # Save data to CSV
            with open('kkday_products.csv', 'w', newline='',encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['City', 'Currency', 'Title', 'Product URL', 'Price'])
                for product in all_products:
                    writer.writerow([product['City'], product['Currency'], product['Title'], product['Product URL'], product['Price']])
        except Exception as e:
            logger.error(f"Error during crawl process: {str(e)}")
        finally:
            logger.info("Closing WebDriver")
            self.driver.quit()

    def crawl_city_currency(self, city, currency):
        url = f"{self.base_url}{city.lower()}"
        logger.info(f"Crawling {url} with currency {currency}")
        products = []
        
        try:
            self.driver.get(url)
            self.zoom_out()
            self.accept_cookies()

            self.change_currency(currency)
            
            # Wait for the product list to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "splide__list"))
            )

            product_items = self.driver.find_elements(By.CLASS_NAME, "splide__slide")
            print(len(product_items))
            for item in product_items:

                if "splide03" not in item.get_attribute("id"):
                    continue

                if item.text == "":
                    continue

                if "is-visible" not in item.get_attribute("class"):
                    self.scroll_right()
                    time.sleep(1)
                    item = self.driver.find_element(By.ID, item.get_attribute("id"))

                title = item.find_element(By.CLASS_NAME, "product-card__title").text
                product_url = item.find_element(By.TAG_NAME, "a").get_attribute("href")
                
                # Extract price
                price_element = item.find_element(By.CSS_SELECTOR, ".kk-price-local__normal")
                price = price_element.text.strip()
                
                # Extract original price if available
                try:
                    original_price_element = item.find_element(By.CSS_SELECTOR, ".kk-price-local__sale .kk-price-origin")
                    original_price = original_price_element.text.strip()
                except NoSuchElementException:
                    original_price = None
                    
                # Extract rating
                rating_element = item.find_element(By.CSS_SELECTOR, ".product-card__info-score")
                rating = rating_element.text.strip()
                        
                # Extract number of reviews
                reviews_element = item.find_element(By.CSS_SELECTOR, ".product-card__info-number")
                reviews = reviews_element.text.strip("()")
                        
                # Extract number of orders
                orders_element = item.find_element(By.CSS_SELECTOR, ".product-card__info-order-number")
                orders = orders_element.text.strip()
                        
                # Extract rank if available
                try:
                    rank_element = item.find_element(By.CLASS_NAME, "product-rank")
                    rank = rank_element.text.strip("TOP ")
                except NoSuchElementException:
                    rank = None
                        
                products.append({
                        'City': city,
                        'Currency': currency,
                        'Rank': rank,
                        'Title': title,
                        'Product URL': product_url,
                        'Price': price,
                        'Original Price': original_price,
                        'Rating': rating,
                        'Reviews': reviews,
                        'Orders': orders
                })
                logger.info(f"Product: {title} - {price}")
    
        except NoSuchElementException as e:
            logger.error(f"Error extracting product info: {str(e)}")
        except TimeoutException:
            logger.error(f"Timeout waiting for page to load: {url}")
        except Exception as e:
            logger.error(f"Error crawling {url}: {str(e)}")

        logger.info(f"Finished crawling {url}")
        
        # Remove duplicates
        unique_products = [dict(t) for t in {tuple(d.items()) for d in products}]
        return unique_products

    def zoom_out(self):
        zoom_out = "document.body.style.zoom='0.5'"
        self.driver.execute_script(zoom_out)
        logger.info("Zoomed out")

    def accept_cookies(self):
        """
        KKDAY has a cookie policy, we need to accept it before we can continue.
        Check the button by id "CybotCookiebotDialogBodyButtonAccept",
        if it exists, click it.
        """
        try:
            time.sleep(2)
            accept_cookies = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "CybotCookiebotDialogBodyButtonAccept"))
            )
            accept_cookies.click()
            logger.info("Accepted cookies")
        except Exception as e:
            pass


    def scroll_right(self):
        """
        the panel only show 4 items at a time, so we need to scroll right to load more products.
        """
        try:
            time.sleep(1)
            self.driver.find_element(By.CSS_SELECTOR, "#splide03 .splide-style-next").click()
            logger.info("Scroll right successfully")
            return True
        except Exception as e:
            logger.error(f"Error scrolling right: {str(e)}")
            return False


    def change_currency(self, currency):
        try:
            time.sleep(5)
            # Find and click the currency dropdown button
            currency_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "header-switch-currency"))
            )
            currency_button.click()

            # Wait for the dropdown to appear and select the desired currency
            currency_option = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, f"header-currency-list-{currency.lower()}"))
            )
            currency_option.click()

            # Wait for the currency to update
            WebDriverWait(self.driver, 10).until(
                EC.text_to_be_present_in_element((By.ID, "header-switch-currency"), currency.upper())
            )

            self.zoom_out()

            logger.info(f"Currency changed to {currency}")
        except Exception as e:
            logger.error(f"Error changing currency to {currency}: {str(e)}")

if __name__ == "__main__":
    crawler = KKDAYCrawler()
    crawler.run()
