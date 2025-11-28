import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.core import driver
from locators.locators import MyInfoPageLocators
from pages.base_page import Base_Page
import logging
from utility.config_reader import get_config

# Create a logger for this module
logger = logging.getLogger(__name__)

class MyInfo_Page(Base_Page):

    def __init__(self,driver):
        """
        Page Object Model (POM) for the 'My Info' Page in OrangeHRM Dashboard.

        Responsibilities:
            - Stores all the locators related to My Info section
            - Contains reusable functions to interact with My Info sidebar
            - Performs validations on UI elements for My Info submodules
        """
        # Store driver instance
        self.driver=driver
        # WebDriverWait to use throughout the class (default 30 sec)
        self.wait = WebDriverWait(self.driver, 30)
        super().__init__(driver)

        # ------------------------- LOCATORS ------------------------------------
        self.my_info_tab = MyInfoPageLocators.MY_INFO_TAB
        self.my_info_menu=MyInfoPageLocators.MY_INFO_MENU
        self.my_info_menu_text=MyInfoPageLocators.MY_INFO_MENU_TEXT
        self.my_info_items = MyInfoPageLocators.MYINFO_ITEMS

        logger.info("MyInfo_Page initialized successfully.")

    # FETCH ALL MY INFO SECTION MENU ITEMS
    @allure.step("Fetching all 'My Info' menu items")
    def get_all_myinfo_items(self):
        """
        Extracts all left-side tabs under My Info section.
        RETURNS:
            A dictionary:
            {
                "Personal Details": WebElement,
                "Contact Details": WebElement,
                "Emergency Contacts": WebElement,
                ...
            }
        """
        logger.info("Collecting My Info menu list items...")
        all_elements = self.find_elements(self.my_info_menu)
        logger.info(f"Found My Info menu elements.")

        myinfo_menu_dict = {}
        for element in all_elements:
            try:
                text_element = element.find_element(*self.my_info_menu_text)
                tab_text = text_element.text.strip()

                if tab_text:
                    myinfo_menu_dict[tab_text] = text_element
                    logger.info(f"My Info tab found: {tab_text}")
            except:
                continue
        logger.info(f"Total My Info menu items extracted: {len(myinfo_menu_dict)}")
        return myinfo_menu_dict

    # OPEN MY INFO MAIN PAGE
    @allure.step("Opening 'My Info' main section")
    def open_myinfo_main(self):
        """
        Clicks the main 'My Info' tab on the left navigation menu.
        """
        logger.info("Opening My Info main menu")
        element = self.is_visible(self.my_info_tab)
        self.click(element)

