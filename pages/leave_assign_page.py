import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from locators.locators import LeaveAssignPageLocators
from pages.base_page import Base_Page
import logging

# Create a logger for this module
logger = logging.getLogger(__name__)

class Leave_Assign_Page(Base_Page):
    def __init__(self,driver):
        """
        Page Object Model for Assign Leave Page.
        Contains:
            - All locators
            - Actions to interact with page
            - Assertions & validation helpers
        """
        # Store driver instance
        self.driver=driver
        # WebDriverWait to use throughout the class (default 30 sec)
        self.wait = WebDriverWait(self.driver, 30)
        super().__init__(driver)

        # --------------------------- Locators --------------------------------------------
        self.leave_menu = LeaveAssignPageLocators.LEAVE_MENU
        self.assign_leave = LeaveAssignPageLocators.ASSIGN_LEAVE

        self.employee_name = LeaveAssignPageLocators.EMPLOYEE_NAME
        self.employee_dropdown_list = LeaveAssignPageLocators.EMPLOYEE_DROPDOWN_LIST

        self.leave_type_dropdown = LeaveAssignPageLocators.LEAVE_TYPE_DROPDOWN
        self.leave_type_options = LeaveAssignPageLocators.LEAVE_TYPE_OPTIONS

        self.from_date_input = LeaveAssignPageLocators.FROM_DATE_INPUT
        self.to_date_input = LeaveAssignPageLocators.TO_DATE_INPUT

        self.comments = LeaveAssignPageLocators.COMMENTS
        self.assign_btn = LeaveAssignPageLocators.ASSIGN_BUTTON

        self.confirm_leave=LeaveAssignPageLocators.CONFIRM_LEAVE
        self.success_msg = LeaveAssignPageLocators.SUCCESS_MSG

        self.leave_list=LeaveAssignPageLocators.LEAVE_LIST
        self.search_button=LeaveAssignPageLocators.SEARCH_BUTTON
        self.search_result_message=LeaveAssignPageLocators.SEARCH_RESULT_MESSAGE
        self.search_result=LeaveAssignPageLocators.SEARCH_RESULT

    # MENU ACTIONS
    @allure.step("Click on Leave menu")
    def click_leave_menu(self):
        logger.info("Clicking Leave Menu")
        element = self.is_visible(self.leave_menu)
        self.action_click(element)

    @allure.step("Click on Assign Leave option")
    def click_assign_leave(self):
        logger.info("Clicking Assign Leave button")
        element = self.is_visible(self.assign_leave)
        self.action_click(element)

    # EMPLOYEE NAME SELECTION
    @allure.step("Entering employee name: {name}")
    def enter_employee_name(self, name):
        logger.info(f"Entering employee name: {name}")
        emp_box = self.is_visible(self.employee_name)
        emp_box.send_keys(name)
        # Wait for autosuggest to load
        options = self.wait_until_all_visible(self.employee_dropdown_list)

        if not options:
            raise Exception("Employee dropdown did not load!")

        logger.info("Selecting first employee suggestion from dropdown")
        actions = ActionChains(self.driver)
        actions.move_to_element(options[0]).pause(2).click().perform()

    # LEAVE TYPE DROPDOWN
    @allure.step("Selecting leave type: {leave_type}")
    def select_leave_type(self, leave_type):
        logger.info(f"Selecting leave type: {leave_type}")
        # Open dropdown
        dropdown = self.wait_until_clickable(self.leave_type_dropdown)
        dropdown.click()

        # locator for option
        option_locator = (By.XPATH, self.leave_type_options.format(leave_type))

        # Wait for an option to appear
        target = self.is_visible(option_locator)

        # Scroll and click using Actions
        actions = ActionChains(self.driver)
        logger.info(f"Clicking on leave type option: {leave_type}")
        actions.scroll_to_element(target).pause(0.3).click(target).perform()

    # DATE INPUT
    @allure.step("Selecting From Date: {date}")
    def select_from_date(self, date):
        logger.info(f"Entering From Date: {date}")
        self.type(self.from_date_input, date)

    @allure.step("Selecting To Date: {date}")
    def select_to_date(self, date):
        logger.info(f"Entering To Date: {date}")
        self.type(self.to_date_input, date)

    # COMMENTS
    @allure.step("Entering comments: {text}")
    def enter_comments(self, text):
        logger.info(f"Entering comments: {text}")
        box = self.is_visible(self.comments)
        box.clear()
        box.send_keys(text)

    # BUTTON CLICKS
    @allure.step("Click Assign button")
    def click_assign_button(self):
        logger.info("Clicking Assign button")
        btn = self.is_visible(self.assign_btn)
        self.action_click(btn)

    @allure.step("Confirming leave assignment")
    def click_confirm_leave(self):
        logger.info("Clicking Confirm Leave button")
        btn = self.is_visible(self.confirm_leave)
        self.action_click(btn)

    # VERIFICATION
    @allure.step("Fetching success message")
    def get_success_message(self):
        try:
            logger.info("Getting success message")
            msg = self.is_visible(self.success_msg)
            return msg.text
        except TimeoutException:
            return None

    @allure.step("Navigate to Leave List page")
    def click_leave_list(self):
        logger.info("Clicking Leave List")
        element = self.is_visible(self.leave_list)
        self.action_click(element)

    @allure.step("Clicking Search button")
    def click_search_button(self):
        logger.info("Clicking Search button")
        element = self.is_visible(self.search_button)
        self.action_click(element)

    @allure.step("Get full search result")
    def search_result(self):
        logger.info("Fetching search result text")
        result = self.is_visible(self.search_result)
        return result.text

    @allure.step("Get search result message")
    def get_search_result(self):
        try:
            logger.info("Reading search result message")
            msg = self.is_visible(self.search_result_message)
            return msg.text
        except TimeoutException:
            return None
