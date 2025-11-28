from selenium.common import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from pages.base_page import Base_Page
from locators.locators import AdminPageLocators
import logging
from selenium.webdriver.support.ui import WebDriverWait
import allure

# Create a logger for this module
logger = logging.getLogger(__name__)

class Admin_Page(Base_Page):
    def __init__(self,driver):
        """
        Page Object Model (POM) for the OrangeHRM Admin Page.

        Responsibilities:
            - Navigation to Admin → User Management → Users
            - Creating new users
            - Selecting dropdown values (Role, Status)
            - Searching & validating users in table
        """
        # Store driver instance
        self.driver=driver
        # WebDriverWait to use throughout the class (default 30 sec)
        self.wait = WebDriverWait(self.driver, 30)
        super().__init__(driver)

        # ---------------- Locators --------------------
        self.admin_menu = AdminPageLocators.ADMIN_MENU
        self.user_management_menu = AdminPageLocators.USER_MANAGEMENT_MENU
        self.users_submenu = AdminPageLocators.USERS_SUBMENU

        self.add_user_button= AdminPageLocators.ADD_USER_BUTTON

        self.role_dropdown= AdminPageLocators.ROLE_DROPDOWN
        self.role_options = AdminPageLocators.ROLE_OPTIONS

        self.status_dropdown = AdminPageLocators.STATUS_DROPDOWN
        self.status_options = AdminPageLocators.STATUS_OPTIONS

        self.employee_name_input = AdminPageLocators.EMPLOYEE_NAME_INPUT
        self.employee_dropdown_option = AdminPageLocators.EMPLOYEE_DROPDOWN_OPTION

        self.username_input = AdminPageLocators.USERNAME_INPUT
        self.password_input = AdminPageLocators.PASSWORD_INPUT
        self.confirm_password_input = AdminPageLocators.CONFIRM_PASSWORD_INPUT

        self.save_button = AdminPageLocators.SAVE_BUTTON
        self.success_message=AdminPageLocators.SUCCESS_MESSAGE

        self.search_username_input = AdminPageLocators.SEARCH_USERNAME_INPUT
        self.search_button = AdminPageLocators.SEARCH_BUTTON
        self.results_rows =AdminPageLocators.RESULT_ROWS

        logger.info("Admin_Page initialized successfully.")

    # OPEN ADMIN MENU
    @allure.step("Opening Admin menu")
    def open_admin_menu(self):
        logger.info("Attempting to open Admin menu.")
        admin_menu = self.is_visible(self.admin_menu)
        self.action_click(admin_menu)
        logger.info("Admin menu opened successfully.")

    # NAVIGATE TO USERS SUBMENU
    @allure.step("Navigating to User Management → Users")
    def navigate_to_users(self):
        logger.info("Navigating to User Management → Users")

        um_menu = self.is_visible(self.user_management_menu)
        self.action_click(um_menu)

        users_submenu = self.is_visible(self.users_submenu)
        self.action_hover(users_submenu)
        logger.info("User Management → Users opened.")

    # CLICK ADD USER BUTTON
    @allure.step("Clicking 'Add User' button")
    def click_add_user(self):
        logger.info("Clicking Add User button.")
        add_btn = self.is_visible(self.add_user_button)
        self.action_click(add_btn)
        logger.info("Add User form opened.")

    # SELECT ROLE
    @allure.step("Selecting user role: {role_name}")
    def select_role(self, role_name):
        logger.info(f"Selecting role: {role_name}")
        # Wait & Click dropdown
        dropdown = self.is_visible(self.role_dropdown)
        dropdown.click()

        # Wait for elements
        options = self.find_elements(self.role_options)

        if not options:
            raise Exception("Role dropdown options did not load!")

        actions = ActionChains(self.driver)

        # Loop and select a required role
        for opt in options:
            if opt.text.strip().lower() == role_name.lower():
                actions.move_to_element(opt).pause(0.2).click().perform()
                logger.info(f"Role selected: {role_name}")
                return True
        raise Exception(f"Role '{role_name}' not found in dropdown options")

    # SELECT STATUS
    @allure.step("Selecting status: {expected_value}")
    def select_status(self, expected_value):
        logger.info(f"Selecting status: {expected_value}")
        # Open dropdown
        dropdown = self.is_visible(self.status_dropdown)
        dropdown.click()

        # Wait for options to appear
        options = self.find_elements(self.status_options)

        if not options:
            raise Exception("Dropdown options did not load")

        actions = ActionChains(self.driver)

        # Loop and select a matching option
        for opt in options:
            if opt.text.strip().lower() == expected_value.lower():
                # Move to option
                actions.move_to_element(opt).pause(0.3).click().perform()
                logger.info(f"Status selected: {expected_value}")
                return True

        raise Exception(f"'{expected_value}' not found in dropdown options")

    # SELECT EMPLOYEE NAME
    @allure.step("Selecting employee name: {emp_name}")
    def select_employee_name(self,emp_name):
        logger.info(f"Selecting employee: {emp_name}")
        actions = ActionChains(self.driver)

        emp_input = self.is_visible(self.employee_name_input)
        emp_input.send_keys(emp_name)
        emp_input.click()

        options = self.wait_until_all_visible(self.employee_dropdown_option)
        if not options:
            raise Exception("Employee dropdown did not load!")

        # Select first dropdown match
        element = options[0]
        actions.move_to_element_with_offset(element, 5, 5).pause(5).click().perform()
        logger.info(f"Employee selected: {emp_name}")

    # FILL NEW USER DETAILS
    @allure.step("Entering new user details for: {username}")
    def new_user_details(self, username, password):
        logger.info(f"Creating new user: {username}")
        # Username
        self.send_keys(self.username_input, username)
        # Password + Confirm
        self.send_keys(self.password_input, password)
        self.send_keys(self.confirm_password_input, password)

    # SAVE USER
    @allure.step("Saving new user")
    def save_user(self):
        logger.info("Saving user details")
        # Save
        self.action_click(self.is_visible(self.save_button))
        logger.info("User saved successfully.")

    # GET SUCCESS MESSAGE
    @allure.step("Fetching success message")
    def get_success_message(self):
        try:
            msg = self.is_visible(self.success_message)
            logger.info(f"Success message found: {msg.text}")
            return msg.text
        except TimeoutException:
            return None

    # SEARCH USER
    @allure.step("Searching for user: {username}")
    def search_user(self, username):
        logger.info(f"Searching user: {username}")

        user = self.is_visible(self.search_username_input)
        user.clear()
        user.send_keys(username)
        self.click(self.search_button)
        logger.info(f"Search initiated for: {username}")

    # VALIDATE USER IN RESULT TABLE
    @allure.step("Validating user '{username}' in result table")
    def is_user_present_in_table(self, username):
        logger.info(f"Checking if user '{username}' is present in table")
        rows = self.wait_until_all_visible(self.results_rows)

        for row in rows:
            row_text = row.text.strip()
            print("ROW:", row_text)

            if username.lower() in row_text.lower():
                logger.info(f"User found in results: {username}")
                return True
        return False

