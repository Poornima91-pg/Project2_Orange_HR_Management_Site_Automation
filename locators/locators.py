from selenium.webdriver.common.by import By

# Login Page Locators
class LoginPageLocators:

    # ---------- Input Fields ----------
    USERNAME_INPUT = (By.NAME, "username")      # Username input field
    PASSWORD_INPUT = (By.NAME, "password")       # Password input field

    # ---------- Login Button ----------
    LOGIN_BUTTON = (By.XPATH, "//button[@type='submit']")       # Login button

    # ---------- Validation Error Messages ----------
    ERROR_MESSAGES = {
        "invalid_credentials": (By.XPATH, "//p[text()='Invalid credentials']"),    # When login fails
        "username_required": (By.XPATH, "(//span[text()='Required'])[1]"),         # Username required error
        "password_required": (By.XPATH, "(//span[text()='Required'])[2]"),         # Password required error
    }

    # ---------- Forgot Password Section ----------
    FORGOT_PASSWORD=(By.XPATH,"//p[text()='Forgot your password? ']")           # Forgot password link
    FORGOT_USERNAME=(By.XPATH,"//input[@placeholder='Username']")               # Username field in reset page
    RESET_PASSWORD_BUTTON=(By.XPATH,"//button[@type='submit']")                 # Submit button for reset
    RESET_SUCCESS_MESSAGE=(By.XPATH,"//h6[text()='Reset Password link sent successfully']")     # Success message

# Dashboard Page Locators
class DashBoardPageLocators:

    # Locators for
    DASHBOARD_LOCATOR = (By.XPATH, "//p[@class='oxd-userdropdown-name']")       # Dashboard username
    PROFILE_ICON = (By.CLASS_NAME, "oxd-userdropdown")                          # Profile dropdown icon
    LOGOUT_BUTTON = (By.XPATH, "//a[text()='Logout']")                          # Logout option

    MENU_ITEMS_TAB=(By.XPATH, "//ul[@class='oxd-main-menu']//child::li")        # All menu items

    # Expected menu items list
    REQUIRED_MENU_ITEMS = ["Admin", "PIM", "Leave", "Time", "Recruitment", "My Info", "Performance", "Dashboard"]

    # Menu text within li tag
    MENU_TEXT_SPAN = (By.XPATH, ".//a//span")

    @staticmethod
    def menu_item_by_text(menu_name: str):
        """
        Returns a dynamic locator for a menu item using visible text.
        """
        return (By.XPATH,f"//ul[@class='oxd-main-menu']//span[text()='{menu_name}']")


#  Admin Page Locators
class AdminPageLocators:

    # ---------- Navigation ----------
    ADMIN_MENU = (By.XPATH, "//span[text()='Admin']")           # Admin menu in sidebar
    USER_MANAGEMENT_MENU = (By.XPATH, "(//span[@class='oxd-topbar-body-nav-tab-item'])[1]")     # User Mgmt top bar
    USERS_SUBMENU = (By.XPATH, "//a[text()='Users']")   # User list submenu

    ADD_USER_BUTTON = (By.XPATH, "(//button[contains(@class,'oxd-button')])[3]")     # Add User button

    # ---------- User Form Fields ----------
    ROLE_DROPDOWN = (By.XPATH, "//label[text()='User Role']/following::div[@class='oxd-select-text-input'][1]")
    ROLE_OPTIONS = (By.XPATH, "//div[@role='option']")          # User role options

    STATUS_DROPDOWN = (By.XPATH, "(//label[text()='Status']/following::div[contains(@class,'oxd-select-text-input')])")
    STATUS_OPTIONS = (By.XPATH,"//div[@role='option']//span | //div[@role='option']")           # Status dropdown options

    EMPLOYEE_NAME_INPUT = (By.XPATH, "//input[@placeholder='Type for hints...']")       # Search employee input
    EMPLOYEE_DROPDOWN_OPTION =  (By.XPATH, "//div[@role='option']")                     # Auto-suggest employee

    USERNAME_INPUT = (By.XPATH, "//label[text()='Username']/following::input[1]")       # Enter username
    PASSWORD_INPUT = (By.XPATH, "//label[text()='Password']/following::input[1]")       # Enter password
    CONFIRM_PASSWORD_INPUT = (By.XPATH, "//label[text()='Confirm Password']/following::input[1]")       # Confirm password

    SUCCESS_MESSAGE = (By.XPATH, "//div[contains(@class,'oxd-toast') and contains(.,'Success')]") # Success message
    SAVE_BUTTON = (By.XPATH, "//button[@type='submit' and contains(@class,'oxd-button')]")   # Save user

    # ---------- Search User Section ----------
    SEARCH_USERNAME_INPUT = (By.XPATH, "//label[text()='Username']/../following-sibling::div/input")
    SEARCH_BUTTON = (By.XPATH, "//button[@type='submit']")

    # Search results table rows
    RESULT_ROWS = (By.XPATH, "//div[@role='table']//div[@role='row']")

# My Info Page Locators
class MyInfoPageLocators:

    MY_INFO_TAB = (By.XPATH, "//span[text()='My Info']")        # My Info menu in sidebar
    MY_INFO_MENU = (By.XPATH, "// div[@class ='orangehrm-tabs']")       # Tabs container

    MY_INFO_MENU_TEXT = (By.XPATH, "//div[ @class ='orangehrm-tabs']//child::a")        # All tabs in My Info

    # Expected MyInfo tab names
    MYINFO_ITEMS = ["Personal Details", "Contact Details", "Emergency Contacts", "Dependents",
                         "Immigration", "Job", "Salary", "Report-to", "Qualifications", "Memberships"]

    @staticmethod
    def myinfo_menu_tab(tab_name: str):
        """Dynamic locator for MyInfo tab."""
        return (By.XPATH, f"//div[@class='orangehrm-tabs']//a[text()='{tab_name}']")

# Leave Assign Locators
class LeaveAssignPageLocators:

    # ---------- Navigation ----------
    LEAVE_MENU = (By.XPATH, "//span[text()='Leave']")           # Main leave menu
    ASSIGN_LEAVE = (By.XPATH, "//a[text()='Assign Leave']")     # Assign leave page

    # ---------- Employee Fields ----------
    EMPLOYEE_NAME = (By.XPATH, "//input[@placeholder='Type for hints...']")          # Employee field
    EMPLOYEE_DROPDOWN_LIST = (By.XPATH, "//div[@role='listbox']//div[@role='option']")

    # ---------- Leave Type Dropdown ----------
    LEAVE_TYPE_DROPDOWN = (By.XPATH,"//label[text()='Leave Type']/../..//div[contains(@class,'oxd-select-text')]")
    # Dynamic leave type option
    LEAVE_TYPE_OPTIONS = "//div[@role='listbox']//span[text()='{}']"

    # ---------- Date Inputs ----------
    FROM_DATE_INPUT = (By.XPATH, "//label[text()='From Date']/following::input[1]")
    TO_DATE_INPUT = (By.XPATH, "//label[text()='To Date']/following::input[1]")

    # ---------- Other Fields ----------
    COMMENTS = (By.XPATH, "//textarea")
    ASSIGN_BUTTON = (By.XPATH, "//button[@type='submit']")
    CONFIRM_LEAVE = (By.XPATH, "(//button[@type='button'])[5]")
    SUCCESS_MSG = (By.XPATH, "//div[contains(@class,'oxd-toast-content--success')]")

    # ---------- Leave List ----------
    LEAVE_LIST = (By.XPATH, "//a[text()='Leave List']")
    SEARCH_BUTTON = (By.XPATH, "//button[@type='submit']")
    SEARCH_RESULT_MESSAGE = (By.XPATH, "//div[@class='oxd-toast-start']//p[text()='No Records Found']")
    SEARCH_RESULT = (By.XPATH, "//div[@class='orangehrm-paper-container']//span[text()='(No Records Found)']")

# Claim Page Locators
class ClaimPageLocators:

        # ---------- Navigation ----------
        CLAIM_MENU = (By.XPATH, "//span[text()='Claim']/parent::a")
        SUBMIT_CLAIM_MENU = (By.XPATH, "//a[text()='Submit Claim']")

        # ---------- Claim Header Section ----------
        CLAIM_TYPE = (By.XPATH,"(//div[@class ='oxd-select-text-input'])[1]")
        CLAIM_TYPE_DROPDOWN=(By.XPATH,"//span[text()='{}']")        # Dynamic claim type

        CURRENCY_TYPE = (By.XPATH, "(//div[@class ='oxd-select-text-input'])[2]")
        CURRENCY_TYPE_DROPDOWN = (By.XPATH, "//div[@role='option']//span[text()='{}']")

        REASON = (By.XPATH, "//textarea")       # Claim reason textarea
        CREATE_CLAIM = (By.XPATH, "//button[text()=' Create ']")
        SUCCESS_MESSAGE = (By.XPATH, "//p[text()='Success']")

        # ---------- Expense Section ----------
        ADD_BUTTON = (By.XPATH, "(//button[text()=' Add '])[1]")

        EXPENSE_TYPE = (By.XPATH, "(//div[@class ='oxd-select-text-input'])[1]")
        EXPENSE_TYPE_DROPDOWN = (By.XPATH, "//div[@role='option']")

        SELECT_DATE = (By.XPATH, "//label[text()='Date']/following::input[1]")          # Date input
        AMOUNT_INPUT = (By.XPATH, "//label[text()='Amount']/following::input[1]")       # Amount input
        NOTES = (By.XPATH, "(//textarea[@class='oxd-textarea oxd-textarea--active oxd-textarea--resize-vertical'])[2]")

        SAVE_BUTTON = (By.XPATH, "//button[@type='submit']")

        # ---------- Submission and History ----------
        SUBMIT_CLAIM=(By.XPATH,"//div[@class='orangehrm-action-buttons-container']//button[text()=' Submit ']")
        CLAIM_HISTORY_ROW = (By.XPATH, "(//div[@class='oxd-table-card'])[1]")       # First claim row
        MY_CLAIMS_TAB = (By.XPATH, "//a[text()='My Claims']")
        LOADER = (By.CSS_SELECTOR, "div.oxd-form-loader")

