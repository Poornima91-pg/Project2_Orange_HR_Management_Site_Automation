import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import (NoSuchElementException,TimeoutException)
from pages.base_page import Base_Page
from locators.locators import LoginPageLocators
from locators.locators import DashBoardPageLocators
import allure

# Create a logger for this module
logger = logging.getLogger(__name__)

class Login_Page(Base_Page):
    def __init__(self,driver):
        """
        Page Object Model class for the Login Page.
        Handles:
        - Locators
        - User actions (enter username/password, click login)
        - Login validations
        - Forgot password flow
        """
        self.driver=driver
        # WebDriverWait to use throughout the class (default 30 sec)
        self.wait = WebDriverWait(self.driver, 30)
        # Call Base Class constructor
        super().__init__(driver)

        # -------------------- Locate Elements --------------------
        # Username,Password & login button locator locator
        self.username_input = LoginPageLocators.USERNAME_INPUT
        self.password_input = LoginPageLocators.PASSWORD_INPUT
        self.login_button = LoginPageLocators.LOGIN_BUTTON

        # Dashboard & error msg locator
        self.error_message = LoginPageLocators.ERROR_MESSAGES
        self.dashboard_locator = DashBoardPageLocators.DASHBOARD_LOCATOR

        self.forgot_password=LoginPageLocators.FORGOT_PASSWORD
        self.forgot_username=LoginPageLocators.FORGOT_USERNAME
        self.reset_password_button=LoginPageLocators.RESET_PASSWORD_BUTTON
        self.reset_success_message=LoginPageLocators.RESET_SUCCESS_MESSAGE

        logger.info("Login_Page POM initialized successfully.")



    # ---------------------- BASIC PAGE ACTIONS ----------------------

    @allure.step("Opening URL page: {url}")
    def navigate_to_url(self,url):
        """Navigate to the homepage URL and wait for it to load."""
        try:
            logger.info(f"Navigating to URL: {url}")
            self.driver.get(url)
            # Use Base_Page method
            self.wait_for_url(url)
            logger.info(f"Successfully navigated to: {url}")

        except TimeoutException as e:
            logger.error(f"Failed to navigate to {url}: {e}")
            raise AssertionError(f"Failed to navigate to URL: {e}")


    @allure.step("Logging in with username: {username}")
    def enter_username(self, username):
        """Enter username"""
        try:
            # Waits for the username field to be visible and enters the provided username
            logger.info(f"Entering username: {username}")
            self.send_keys(self.username_input,username)
        except (TimeoutException, NoSuchElementException):
            print("Username field not found")
            return False
        return True


    @allure.step("Entering password")
    def enter_password(self, password):
        """Enter password"""
        try:
            # Waits for the password field to be visible and enters the provided password
            logger.info("Entering password")
            self.send_keys(self.password_input,password)
        except (TimeoutException, NoSuchElementException):
            print("Password field not found")
            return False
        return True


    @allure.step("Clicking login button")
    def click_login(self):
        try:
            # self.enter_username(username)
            # self.enter_password(password)
            self.click(self.login_button)
        except (TimeoutException, NoSuchElementException):
            print("Login button not clickable")
            return False
        return True

    # ---------------------- LOGIN STATUS VALIDATION ----------------------
    def get_login_status(self):
        """
        Determines whether login was successful.
        Returns:
        - "Success"       - Dashboard loaded
        - Unsuccessful    - error message
        """
        logger.info("Checking login status...")

        # --------- SUCCESS CHECK ---------
        try:
            self.is_visible(self.dashboard_locator)
            if "dashboard" in self.get_current_url().lower():
                logger.info("Login successful")
                return "Success"

        except TimeoutException:
            pass

        # --------- ERROR MESSAGES ---------
        for key, locator in self.error_message.items():
            try:
                error_element = self.is_visible(locator)
                if error_element:
                    msg = error_element.text.strip()
                    logger.info(f"Login failed → Error: {msg}")
                    return msg
            except TimeoutException:
                continue
        logger.error("Login failed: Unknown error")
        return "Failed: Unknown error"

    # ---------------------- FORGOT PASSWORD FLOW -------------------------
    @allure.step("Clicking Forgot Password link")
    def forgot_password_link(self):
        """Click on 'Forgot Password' link."""
        logger.info("Opening Forgot Password page")
        self.is_visible(self.forgot_password)
        self.click(self.forgot_password)

    @allure.step("Resetting password for username: {username}")
    def reset_password_username(self,username):
        """Enter username and click reset password."""
        logger.info(f"Entering username for password reset: {username}")
        self.is_visible(self.forgot_username)
        self.send_keys(self.forgot_username,username)

        logger.info("Clicking reset password button")
        self.is_visible(self.reset_password_button)
        self.click(self.reset_password_button)

    @allure.step("Verifying reset password success message")
    def reset_success(self):
        """Return success reset password message."""
        logger.info("Checking reset success message")
        success_message=self.is_visible(self.reset_success_message)

        if success_message:
            logger.info(f"Reset success: {success_message.text.strip()}")
            return success_message.text.strip()
        else:
            return None






