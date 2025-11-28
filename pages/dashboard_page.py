import logging
from selenium.webdriver.support.ui import WebDriverWait
from pages.base_page import Base_Page
from locators.locators import DashBoardPageLocators
import allure

# Create a logger for this module
logger = logging.getLogger(__name__)

class Dashboard_Page(Base_Page):
    def __init__(self,driver):
        """
        Page Object Model (POM) class for the OrangeHRM Dashboard Page.

        Contains:
            • Locators related to the dashboard page
            • Reusable utility methods to interact with dashboard elements
            • Assertions/validations for dashboard-specific features
        """

        # Store driver instance
        self.driver=driver
        # WebDriverWait to use throughout the class (default 30 sec)
        self.wait = WebDriverWait(self.driver, 30)
        super().__init__(driver)

        # ------------------------- LOCATORS ------------------------------------
        self.profile_icon = DashBoardPageLocators.PROFILE_ICON
        self.logout_button = DashBoardPageLocators.LOGOUT_BUTTON
        self.dashboard_locator = DashBoardPageLocators.DASHBOARD_LOCATOR
        self.menu_items_tab=DashBoardPageLocators.MENU_ITEMS_TAB
        self.required_menu_items=DashBoardPageLocators.REQUIRED_MENU_ITEMS
        self.menu_text_span=DashBoardPageLocators.MENU_TEXT_SPAN

        logger.info("Dashboard_Page initialized successfully.")


    # LOGOUT FUNCTIONALITY
    @allure.step("Performing logout action from dashboard")
    def perform_logout(self):
        """
        Logs out the user by clicking the profile icon and then logout button.
        RETURNS:
        True → Logout successful
        False → Logout failed
        """
        logger.info("Attempting to logout user...")
        try:
            self.click(self.profile_icon)
            self.click(self.logout_button)
            logger.info("Logout successful.")
            return True
        except:
            return False

    # DASHBOARD STATUS CHECK
    @allure.step("Checking if dashboard is loaded")
    def is_dashboard_loaded(self):
        """
        Checks whether the dashboard page is visible.
        RETURNS:
        True → Dashboard is loaded
        """
        logger.info("Verifying if dashboard is loaded...")
        return self.is_visible(self.dashboard_locator)

    # MENU EXTRACTION LOGIC
    @allure.step("Fetching all menu items from left navigation panel")
    def get_all_menu_items(self):
        """
        Extracts all menu items from the left navigation bar.
        RETURNS:
            A dictionary in this format:
            {
                "Admin": WebElement,
                "PIM": WebElement,
                "Leave": WebElement,
                ...
            }
        """
        logger.info("Collecting all menu items from dashboard...")
        # Fetch all <li> elements representing menu items
        all_li_elements = self.find_elements(self.menu_items_tab)

        menu_dict = {}
        for li in all_li_elements:
            try:
                # Each li has a span containing menu text
                text_element = li.find_element(*self.menu_text_span)
                menu_text = text_element.text.strip()

                if menu_text:
                    menu_dict[menu_text] = text_element
            except:
                continue

        logger.info(f"Total extracted menu items: {len(menu_dict)}")
        return menu_dict

