import pytest
from selenium import webdriver

from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService

from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from utility.config_reader import get_config    #To read browser from config.ini
import logging

# Configure logging inside setup
logger = logging.getLogger(__name__)

def pytest_addoption(parser):
    """
    Pytest hook to add a command-line option for browser name.
    This allows passing --browser-name at runtime.
    Example:
    pytest -v --browser-name chrome
    """
    parser.addoption(
        "--browser-name",default = 'chrome', help="This will take browser name from user"
    )

@pytest.fixture(scope='class') # set up and tear down
def setup(request):
    """
    Pytest fixture to set up and tear down the Selenium WebDriver.

    PROCESS:
    1. Read browser name from CLI or config.ini.
    2. Setup the correct WebDriver with appropriate options.
    3. Apply window maximize + implicit wait.
    4. Attach driver to test class.
    5. Return driver to test.
    6. Quit driver after test completion.
    """
    driver = None
    logger.info("========== TEST SETUP STARTED ==========")
    try:
        # Get browser from Command line first, else from config file
        browser_name = request.config.getoption("--browser-name") or get_config("browser_name", "browser")
        logger.info(f"Selected browser: {browser_name}")
        browser = browser_name.lower()

        # Initialize the driver based on browser name
        #  Launching Chrome
        if browser == 'chrome':

            logger.info("Initializing Chrome browser...")
            options = ChromeOptions()
            # Open browser in Incognito mode
            options.add_argument("--incognito")
            # Disable password manager popup
            options.add_experimental_option("prefs", {
                "credentials_enable_service": False,
                "profile.password_manager_enabled": False
            })
            # WebDriverManager auto-installs correct driver version
            driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=options)
            logger.info("Launched Chrome browser in incognito mode")

        #  Launching Firefox
        elif browser == 'firefox':
            logger.info("Initializing Firefox browser...")
            options = FirefoxOptions()
            # Open Firefox in private mode
            options.set_preference("browser.privatebrowsing.autostart", True)

            driver = webdriver.Firefox(
                service=FirefoxService(GeckoDriverManager().install()),
                options=options
            )
            logger.info("Launched Firefox in private mode")

        #  Launching Edge
        elif browser == 'edge':
            logger.info("Initializing Edge browser...")
            options = EdgeOptions()
            options.add_argument("--inprivate")
            driver = webdriver.Edge(
                service=EdgeService(),
                options=options
            )
            logger.info("Launched Edge in InPrivate mode")

        else:
            raise ValueError(f"Unsupported browser: {browser_name}")

        # Browser window setup
        driver.maximize_window()
        driver.implicitly_wait(10)

        # Attach the driver to the class so page objects can access it
        request.cls.driver = driver

        logger.info("========== TEST SETUP COMPLETED ==========")
        # Yield to test, then teardown
        yield driver

    except Exception as e:
        # Log unexpected errors during setup
        logger.exception(f"Error occurred while launching browser: {e}")
        raise

    finally:
        # Quit the browser after test completion
        if driver:
            logger.info("========== TEARDOWN: Closing Browser ==========")
            logging.info("Closing the browser")
            driver.quit()


def pytest_configure():
    """
    Pytest to configure logging before tests start.
    Configure the root logger to log INFO and above level messages to both file and console.
    Sets up both file and console handlers with a common formatter.
    """
    try:
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(name)s - %(message)s')

        # File handler for saving logs to file
        file_handler = logging.FileHandler("test_logs.log")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # Console handler to print logs on terminal
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        logger.info("Logging configured successfully")

    except Exception as e:
        print(f"Failed to configure logging: {e}")