from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException,ElementClickInterceptedException
import allure
import logging
from selenium.webdriver.common.action_chains import ActionChains as actions
from selenium.webdriver.common.keys import Keys

# Set up logger for this test module
logger = logging.getLogger(__name__)


class Base_Page:
    """
       Base Page class provides reusable Selenium utilities for
       all Page Object classes:
       - Clicks
       - Send Keys
       - Waits
       - Visibility checks
       - Action Chains
       - Allure reporting helpers
       """

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 30)

    # CLICK OPERATION
    def click(self, locator):
        """
            Click on an element located by `locator`.
            Raises AssertionError if not clickable.
            """
        with allure.step(f"Clicking element → {locator}"):
            try:
                logger.info(f"Clicking on element: {locator}")
                element = self.wait.until(EC.element_to_be_clickable(locator))
                element.click()
                return  element
            except (TimeoutException, ElementClickInterceptedException) as e:
                raise AssertionError(f"Cannot click element {locator}: {e}")

    # SEND KEYS
    def send_keys(self, locator,text):
        """
        Sends text to a field.
        Clears the field before typing.
        """
        with allure.step(f"Entering text into element → {locator}"):
            try:
                logger.info(f"Sending keys to {locator}: {text}")
                element = self.is_visible(locator)
                element.clear()
                element.send_keys(text)
            except TimeoutException as e:
                raise AssertionError(f"Cannot send keys to element {locator}: {e}")

    # URL HANDLING
    def get_current_url(self):
        """Returns the current page URL."""
        logger.info("Fetching current URL")
        return self.driver.current_url

    def wait_for_url(self, expected_url):
        """
            Waits until the URL matches the expected URL.
        """
        with allure.step(f"Waiting for URL → {expected_url}"):
            logger.info(f"Waiting for URL to be: {expected_url}")
            try:
                self.wait.until(EC.url_to_be(expected_url))
            except TimeoutException:
                raise AssertionError(f"Timed out waiting for URL {expected_url}")

    # VISIBILITY CHECK
    def is_visible(self, locator):
        """
            Waits until an element is visible on the page.
            Returns the element or None if not visible.
        """
        logger.info(f"Checking visibility for element: {locator}")
        try:
            element = self.wait.until(EC.visibility_of_element_located(locator))
            return element
        except TimeoutException:
            return None

    # DISPLAY + ENABLE CHECK
    def element_is_displayed_and_enabled(self, locator):
        """
            Returns True if element is both displayed and enabled (clickable)
        """
        logger.info(f"Checking if element is displayed & enabled: {locator}")
        try:
            element = self.wait.until(EC.element_to_be_clickable(locator))
            return element.is_displayed() and element.is_enabled()
        except Exception as e:
            logger.error(f"Element not ready for interaction: {locator} → {e}")
            return False

    # FIND MULTIPLE ELEMENTS
    def find_elements(self, locator):
        """Returns list of elements located by the locator."""
        logger.info(f"Finding elements with locator: {locator}")
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    # ALLURE SCREENSHOT ATTACHMENT
    def attach_save_screenshot(self, name='screenshot'):
        """
        Takes screenshot and attaches it to Allure Report.
        """
        logger.info(f"Capturing screenshot → {name}")
        try:
            file_path = f"screenshots/{name}.png"
            self.driver.save_screenshot(file_path)
            png = self.driver.get_screenshot_as_png()
            allure.attach(png, name=name, attachment_type=allure.attachment_type.PNG)
        except:
            logger.error(f"Screenshot capture failed:")
            pass

    # WAIT FOR ALL ELEMENTS VISIBLE
    def wait_until_all_visible(self, locator):
        """
        Returns list of visible elements.
        Returns empty list if timeout.
        """
        logger.info(f"Waiting for all elements visible: {locator}")
        try:
            elements = self.wait.until(EC.visibility_of_all_elements_located(locator))
            return elements
        except TimeoutException:
            return []

    # ACTION CHAIN WRAPPERS
    def action_hover(self, element):
        """Hover over an element."""
        logger.info(f"Hovering over element: {element}")
        with allure.step("Hover over element"):
            actions(self.driver).move_to_element(element).perform()

    def action_click(self, element):
        """Perform ActionChain click."""
        logger.info(f"Action click on element: {element}")
        with allure.step("Action click element"):
            actions(self.driver).move_to_element(element).pause(0.2).click().perform()

    # TYPE VALUE AND ENTER
    def type(self, locator, value):
        """
        Types into a field and presses ENTER.
        """
        with allure.step(f"Typing '{value}' into element → {locator}"):
            logger.info(f"Typing into {locator}: {value}")
            element = self.wait.until(EC.visibility_of_element_located(locator))
            element.clear()
            element.send_keys(value)
            element.send_keys(Keys.ENTER)

    # WAIT FOR CLICKABLE
    def wait_until_clickable(self, locator):
        """
        Waits until locator is clickable and returns element.
        """
        logger.info(f"Waiting for element clickable: {locator}")
        try:
            return self.wait.until(EC.element_to_be_clickable(locator))
        except TimeoutException:
            raise TimeoutException(f"Element not clickable: {locator}")

    # ELEMENT PRESENCE CHECK
    def is_present(self,locator):
        """
        Checks if an element is present in DOM.
        """
        logger.info(f"Checking presence of element: {locator}")
        try:
            return self.wait.until(EC.presence_of_element_located(locator))
        except TimeoutException:
            return None


