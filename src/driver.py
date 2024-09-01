from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
import random
from logger import setup_logger

logger = setup_logger()

def create_driver():
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
#    chrome_options.add_argument("--headless=new")  # Always run in headless mode

    # Anti-crawler configurations
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    # Set a random user agent
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
    ]
    chrome_options.add_argument(f"user-agent={random.choice(user_agents)}")

    # Create a new instance of the Chrome driver
    chromedriver_autoinstaller.install()
    driver = webdriver.Chrome(options=chrome_options)

    # Additional settings after driver creation
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": random.choice(user_agents)})

    driver.maximize_window() 
    driver.implicitly_wait(10)

    logger.info("Selenium WebDriver created successfully in headless mode")
    return driver

if __name__ == "__main__":
    # Example usage
    driver = create_driver()
    driver.get("https://www.example.com")
    print(driver.title)
    driver.quit()