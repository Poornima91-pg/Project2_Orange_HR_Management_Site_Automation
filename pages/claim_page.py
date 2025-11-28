from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import allure
from locators.locators import ClaimPageLocators
from pages.base_page import Base_Page
import logging

# Create a logger for this module
logger = logging.getLogger(__name__)

class Claim_Page(Base_Page):
    def __init__(self,driver):
        """
        Page Object Model for the Claim Page.
        Contains:
            - All claim-related web elements (locators)
            - Reusable actions to interact with claim UI
            - Validation and helper methods
        """
        # Store driver instance
        self.driver=driver
        # WebDriverWait to use throughout the class (default 30 sec)
        self.wait = WebDriverWait(self.driver, 30)
        super().__init__(driver)

        # ---------------- Locators ----------------
        self.claim_menu = ClaimPageLocators.CLAIM_MENU
        self.submit_claims_menu = ClaimPageLocators.SUBMIT_CLAIM_MENU

        self.claim_type= ClaimPageLocators.CLAIM_TYPE
        self.claim_type_dropdown=ClaimPageLocators.CLAIM_TYPE_DROPDOWN

        self.currency_type=ClaimPageLocators.CURRENCY_TYPE
        self.currency_type_dropdown = ClaimPageLocators.CURRENCY_TYPE_DROPDOWN

        self.reason=ClaimPageLocators.REASON

        self.create_claim=ClaimPageLocators.CREATE_CLAIM
        self.success_message=ClaimPageLocators.SUCCESS_MESSAGE

        self.add_button=ClaimPageLocators.ADD_BUTTON

        self.expense_type=ClaimPageLocators.EXPENSE_TYPE
        self.expense_type_dropdown = ClaimPageLocators.EXPENSE_TYPE_DROPDOWN

        self.select_date=ClaimPageLocators.SELECT_DATE

        self.amount_input=ClaimPageLocators.AMOUNT_INPUT
        self.notes=ClaimPageLocators.NOTES

        self.save_button=ClaimPageLocators.SAVE_BUTTON
        self.submit_claim =ClaimPageLocators.SUBMIT_CLAIM

        self.claim_history_row = ClaimPageLocators.CLAIM_HISTORY_ROW
        self.my_claims = ClaimPageLocators.MY_CLAIMS_TAB
        self.loader = ClaimPageLocators.LOADER

    # NAVIGATION METHODS
    @allure.step("Navigate to Claim → Submit Claim")
    def open_claim_section(self):
        logger.info("Opening Claim module")
        self.click(self.claim_menu)

        logger.info("Opening Submit Claim page")
        self.click(self.submit_claims_menu)

    # CLAIM TYPE SELECTION
    @allure.step("Select Claim Type: {claim_type}")
    def select_claim_type(self, claim_type):
        logger.info(f"Selecting Claim Type: {claim_type}")
        self.click(self.claim_type)
        option = (By.XPATH, self.claim_type_dropdown[1].format(claim_type))
        self.click(option)

    # CURRENCY TYPE SELECTION
    @allure.step("Select Currency Type: {currency_type}")
    def select_currency_type(self, currency_type):
        logger.info(f"Selecting Currency Type: {currency_type}")
        self.click(self.currency_type)
        option = (By.XPATH, self.currency_type_dropdown[1].format(currency_type))
        self.click(option)

    # REMARKS / REASON
    @allure.step("Enter Remarks: {reason}")
    def enter_remarks(self,reason):
        logger.info(f"Entering reason: {reason}")
        self.send_keys(self.reason,reason)

    # CREATE CLAIM
    @allure.step("Click on Create Claim button")
    def create_submit_claim(self):
        logger.info("Clicking Create Claim button")
        self.click(self.create_claim)

    # SUBMIT CLAIM
    @allure.step("Submit Claim")
    def click_submit_claim(self):
        logger.info("Submitting claim")
        self.wait_for_no_loader()
        self.click(self.submit_claim)

    # SAVE CLAIM
    @allure.step("Save Claim")
    def save_claim(self):
        logger.info("Clicking Save button for claim")
        self.wait_for_no_loader()
        self.click(self.save_button)

    # SUCCESS MESSAGE
    @allure.step("Get Success Message")
    def get_success_message(self):
        try:
            logger.info("Fetching success message after claim save/submit")
            msg = self.is_visible(self.success_message)
            return msg.text
        except TimeoutException:
            return None

    # ADD EXPENSE
    @allure.step("Click Add Expense button")
    def add_expense(self):
        logger.info("Adding new expense row inside claim")
        self.click(self.add_button)

    # EXPENSE DATE SELECTION
    @allure.step("Select Claim Date: {date}")
    def select_claim_date(self, date):
        logger.info(f"Selecting claim date: {date}")
        element = self.wait_until_clickable(self.select_date)
        element.click()
        element.send_keys(date)  # enter new date
        element.send_keys(Keys.ENTER)  # close date picker popup

    # AMOUNT ENTRY
    @allure.step("Enter Claim Amount: {amount}")
    def enter_amount(self, amount):
        logger.info(f"Entering claim amount: {amount}")
        element=self.wait_until_clickable(self.amount_input)
        element.click()
        element.send_keys(amount)
        element.send_keys(Keys.ENTER)

    # NOTES ENTRY
    @allure.step("Enter Notes: {reason}")
    def enter_notes(self,reason):
        logger.info(f"Entering notes: {reason}")
        self.send_keys(self.notes, reason)

    # CLAIM HISTORY
    @allure.step("Navigate to Claim History")
    def navigate_to_claim_history(self):
        logger.info("Navigating to My Claims (Claim History)")
        self.click(self.my_claims)

    @allure.step("Verify Claim appears in Claim History")
    def verify_claim_in_history(self,claim_type,currency):
        logger.info("Validating claim entry from history table")
        rows = self.wait_until_all_visible(self.claim_history_row)

        for row in rows:
            row_text = row.text.strip().lower()
            print("ROW:", row_text)

            if claim_type.lower() in row_text and currency.lower() in row_text:
                logger.info("Match found in Claim History")
                return True

        return False

    # LOADER WAIT METHOD
    @allure.step("Waiting for loader to disappear")
    def wait_for_no_loader(self):
        logger.info("Waiting for loader to disappear")
        try:
            self.wait.until(EC.invisibility_of_element_located(self.loader))
        except:
            pass
