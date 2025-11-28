import pytest
import logging
import allure
from locators.locators import DashBoardPageLocators
from locators.locators import MyInfoPageLocators
from utility.config_reader import get_config
from utility.excel_reader import ExcelUtil
from pages.base_page import Base_Page
from pages.login_page import Login_Page
from pages.dashboard_page import Dashboard_Page
from pages.admin_page import Admin_Page
from pages.leave_assign_page import Leave_Assign_Page
from pages.myinfo_page import MyInfo_Page
from pages.claim_page import Claim_Page

# Set up logger for this test module
logger = logging.getLogger(__name__)

excel_path = get_config("Excel", "path")
sheet = get_config("Excel", "sheet")
excel = ExcelUtil(excel_path, sheet)
excel_row_valid = ExcelUtil(excel_path, sheet).get_row(2)

@pytest.mark.usefixtures("setup")
class Test_Orange_Hrsite_Automation_DashBoard_Page:

    # -------------------------------- TC 4----------------------------------
    #  Validate Menu items visibility

    @allure.title("TC04 – Validate Menu Items Visibility, Click & URL Navigation")
    @allure.description("Verifies the visibility, clickability, and correct URL navigation of all main menu items.")
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.parametrize("row,username,password", excel_row_valid)
    def test_tc04_validate_menu_items_visibility_and_urls(self, setup, row, username, password):

        driver = setup
        basepage = Base_Page(driver)
        dashboardpage = Dashboard_Page(driver)

        # CONFIG DATA
        login_url = get_config("Login_Orange", "url")
        dashboard_url = get_config("Dashboard_Page", "url")

        # LOGIN STEP
        with allure.step("Login to HRM Application"):
            logger.info("=== Starting Login Process ===")

            loginpage = Login_Page(driver)
            loginpage.navigate_to_url(login_url)

            logger.info(f"Entering username: {username}")
            loginpage.enter_username(username)

            logger.info(f"Entering password")
            loginpage.enter_password(password)

            logger.info("Clicking the Login button")
            loginpage.click_login()

            # Wait until Dashboard URL loads
            logger.info("Waiting for Dashboard page to load...")
            basepage.wait_for_url(dashboard_url)

        # URL mapping for validation
        url_map = {
            "Admin": get_config("Menu_URLs", "admin"),
            "PIM": get_config("Menu_URLs", "pim"),
            "Leave": get_config("Menu_URLs", "leave"),
            "Time": get_config("Menu_URLs", "time"),
            "Recruitment": get_config("Menu_URLs", "recruitment"),
            "My Info": get_config("Menu_URLs", "myinfo"),
            "Performance": get_config("Menu_URLs", "performance"),
            "Dashboard": get_config("Menu_URLs", "dashboard")
        }

        logger.info("=== Starting Menu Validation Loop ===")

        # LOOP THROUGH MENU ITEMS
        for menu_name in dashboardpage.required_menu_items:

            with allure.step(f"Validate menu: {menu_name}"):
                try:
                    logger.info(f"Validating menu → {menu_name}")

                    # Re-fetch locator every loop
                    locator = DashBoardPageLocators.menu_item_by_text(menu_name)

                    # VALIDATE VISIBILITY + ENABLED
                    logger.info(f"Checking if '{menu_name}' is displayed and enabled")

                    assert basepage.element_is_displayed_and_enabled(locator), \
                    f"{menu_name} is not visible/enabled"

                    logger.info(f"{menu_name} is visible and enabled")

                    basepage.attach_save_screenshot(f"TC_04_{menu_name}_Visible_Enabled_success")

                    # CLICK
                    basepage.click(locator)
                    logger.info(f"Clicked {menu_name}")

                    # URL VALIDATE
                    expected_url = url_map[menu_name]
                    logger.info(f"Expected URL for '{menu_name}' → {expected_url}")

                    basepage.wait_for_url(expected_url)
                    actual_url = basepage.get_current_url()

                    logger.info(f"Actual URL after clicking: {actual_url}")

                    assert actual_url == expected_url, \
                    f"URL Mismatch for {menu_name}: Expected {expected_url}, Got {actual_url}"

                    logger.info(f"URL validated for {menu_name}")
                    basepage.attach_save_screenshot(f"TC04_{menu_name}_URL_success")

                except Exception as e:
                    basepage.attach_save_screenshot(f"TC04_{menu_name}_Failed")
                    logger.error(f"Error in {menu_name}: {e}")
                    raise

    # -----------------------------------TC_08--------------------------------
    # My Info page menu items Visibility & Navigation validation

    @allure.title("TC08 – Validate My Info Menu Items Visibility & Navigation")
    @allure.description(
        "Verifies all sub-menu items under My Info are present, clickable, and navigate to correct URLs.")
    @pytest.mark.regression
    @pytest.mark.usefixtures("setup")
    @pytest.mark.parametrize("row,username,password", excel_row_valid)
    def test_tc08_validate_myinfo_menu(self, setup, row, username, password):
        driver = setup
        basepage = Base_Page(driver)
        myinfopage = MyInfo_Page(driver)

        # LOGIN IS ALREADY DONE BY FIXTURE
        # OPEN MY INFO
        with allure.step("Open My Info main section"):
            logger.info("Opening 'My Info' main menu")
            myinfopage.open_myinfo_main()

        # URL MAP FOR VALIDATION
        myinfo_urls = {
            "Personal Details": get_config("MYINFO_URLS", "personal_details"),
            "Contact Details": get_config("MYINFO_URLS", "contact_details"),
            "Emergency Contacts": get_config("MYINFO_URLS", "emergency_contacts"),
            "Dependents": get_config("MYINFO_URLS", "dependents"),
            "Immigration": get_config("MYINFO_URLS", "immigration"),
            "Job": get_config("MYINFO_URLS", "job"),
            "Salary": get_config("MYINFO_URLS", "salary"),
            "Report-to": get_config("MYINFO_URLS", "report_to"),
            "Qualifications": get_config("MYINFO_URLS", "qualifications"),
            "Memberships": get_config("MYINFO_URLS", "memberships"),
        }

        logger.info("=== Starting My Info Tab Validation Loop ===")

        # LOOP THROUGH ALL TABS
        for tab_name in myinfopage.my_info_items:

            try:
                logger.info(f"Validating My Info tab → {tab_name}")

                # RE-FETCH LOCATOR EACH LOOP
                locator = MyInfoPageLocators.myinfo_menu_tab(tab_name)

                # VALIDATE VISIBILITY & CLICKABILITY
                logger.info(f"Checking if '{tab_name}' is displayed and enabled")
                assert basepage.element_is_displayed_and_enabled(locator), \
                    f"{tab_name} is not visible/enabled"
                logger.info(f"{tab_name} is visible and enabled")

                basepage.attach_save_screenshot(f"TC_08_{tab_name}_Visible_Enabled_success")

                # CLICK
                basepage.click(locator)
                logger.info(f"Clicked {tab_name}")

                # URL VALIDATION
                expected_url = myinfo_urls[tab_name]
                logger.info(f"Expected URL for '{tab_name}' → {expected_url}")

                basepage.wait_for_url(expected_url)
                actual_url = basepage.get_current_url()
                logger.info(f"Actual URL after clicking: {actual_url}")

                assert actual_url == expected_url, \
                    f"URL Mismatch for {tab_name}: Expected {expected_url}, Got {actual_url}"

                logger.info(f"URL validated for {tab_name}")
                basepage.attach_save_screenshot(f"TC08_{tab_name}_URL_success")

            except Exception as e:
                basepage.attach_save_screenshot(f"TC_08_{tab_name}_Failure")
                logger.error(f"Error in {tab_name}: {e}")
                raise

    # ---------------------------------------------- TC-09----------------------------------------
    # Assig Leave and validate in search result

    @allure.title("TC09 – Validate Assign Leave & Search Result")
    @allure.description("Validates assigning leave for an employee and verifying it in the search list.")
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.parametrize("row,username,password", excel_row_valid)
    def test_tc09_validate_assign_leave(self, setup, row, username, password):

        driver = setup
        basepage = Base_Page(driver)
        leave_page = Leave_Assign_Page(driver)

        # config data
        expected_msg = get_config("Leave_Data", "success_message")
        employee_name = get_config("Leave_Data", "employee_name")
        leave_type = get_config("Leave_Data", "leave_type")
        from_date = get_config("Leave_Data", "from_date")
        to_date = get_config("Leave_Data", "to_date")
        comment_text = get_config("Leave_Data", "comments")
        search_message = get_config("Leave_Data", "search_message")

        logger.info("Logged in as Admin.")
        logger.info("=== TC09 – Starting Assign Leave Test ===")

        # Navigate to Assign Leave
        with allure.step("Navigate to Assign Leave section"):
            logger.info("Navigating to Leave module → Assign Leave page...")
            leave_page.click_leave_menu()
            leave_page.click_assign_leave()
            logger.info("Navigated to Leave → Assign Leave page")

        # Enter Employee Name
        with allure.step("Enter employee name and select from autocomplete"):
            logger.info(f"Selecting employee: {employee_name}")
            leave_page.enter_employee_name(employee_name)
            logger.info(f"Employee selected: {employee_name}")

        # Select Leave Type
        with allure.step("Select Leave Type from dropdown"):
            logger.info(f"Selecting leave type: {leave_type}")
            leave_page.select_leave_type(leave_type)
            logger.info(f"Leave type selected: {leave_type}")

        # Enter Dates
        with allure.step("Enter From and To dates"):
            logger.info(f"Entering date range: From={from_date}, To={to_date}")
            leave_page.select_from_date(from_date)
            logger.info(f"Dates selected: From {from_date} To {to_date}")

        #  Add Comments
        with allure.step("Enter comments for leave"):
            logger.info("Entering comments...")
            leave_page.enter_comments(comment_text)
            logger.info("Comments entered.")

        # Click Assign Button
        with allure.step("Submit leave assignment"):
            logger.info("Clicking Assign button...")

            leave_page.click_assign_button()
            leave_page.click_confirm_leave()

            logger.info("Leave assignment submitted.")
            basepage.attach_save_screenshot("TC09_Leave_Assign_success")

        # Validate Success Message
        with allure.step("Validate success toast message"):
            logger.info("Reading success toast...")
            success_text = leave_page.get_success_message()

            logger.info("Success message received: " + success_text)

            assert success_text is not None, "Success toast not visible"
            assert expected_msg in success_text, f"Expected success message '{expected_msg}' not found"

        # Validate Assigned Leave in Search List
            with allure.step("Validate Assigned Leave in Search List"):
                logger.info("Navigating to Leave List page...")
                leave_page.click_leave_list()
                leave_page.enter_employee_name(employee_name)
                leave_page.click_search_button()

                logger.info("Fetching search results...")
                report_text = leave_page.get_search_result()

                assert report_text is not None, "report text mismatch"
                assert search_message in report_text, f"Search message mismatch: Expected '{search_message}'"

                basepage.attach_save_screenshot("TC09_Leave_Search_Validation_success")

        logger.info("==== TC09 Leave Assignment Validated Successfully ====")

    # -------------------------------- TC_05--------------------------------
    # new user creation in admin page

    @allure.title("TC05 – Validate New User Creation & Login Functionality")
    @allure.description(
        "Creates a new user from Admin → User Management and validates login with the newly created user.")
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_tc05__create_and_validate_new_user(self, setup):

        driver = setup
        basepage = Base_Page(driver)
        loginpage = Login_Page(driver)
        adminpage = Admin_Page(driver)
        dashboardpage = Dashboard_Page(driver)

        logger.info("====== TC05: Create and Validate New User Test Started ======")

        # CONFIG VALUES
        login_url = get_config("Login_Orange", "url")
        dashboard_url = get_config("Dashboard_Page", "url")
        role = get_config("Add_new_user", "role")
        status = get_config("Add_new_user", "status")
        employee_name = get_config("Add_new_user", "emp_name")
        new_username = get_config("Add_new_user", "new_username")
        new_password = get_config("Add_new_user", "new_password")
        admin_url = get_config("Add_new_user", "admin_url")
        add_url = get_config("Add_new_user", "add_url")
        expected_msg = get_config("Add_new_user", "success_message")

        # Navigate to Admin → Add User
        with allure.step("Navigate to Admin → Add User"):
            logger.info("Navigating to Admin menu...")
            adminpage.open_admin_menu()

            logger.info("Opening User Management page...")
            adminpage.navigate_to_users()

            logger.info("Clicking Add User button...")
            adminpage.click_add_user()

            logger.info("Admin Add User page loaded.")

        # Fill in new user details
        with allure.step("Enter New User Form Details"):
            logger.info("Waiting for Add User form to load...")
            basepage.wait_for_url(add_url)

            logger.info(f"Selecting Role: {role}")
            adminpage.select_role(role)

            logger.info(f"Selecting Status: {status}")
            adminpage.select_status(status)

            logger.info(f"Entering Employee Name: {employee_name}")
            adminpage.select_employee_name(employee_name)

            logger.info(f"Entering New Username: {new_username}")
            logger.info("Entering New Password...")
            adminpage.new_user_details(new_username, new_password)

            logger.info("New user details entered successfully.")

        # Save New User & Validate Success Message
        with allure.step("Save New User and Validate Success Message"):
            adminpage.save_user()
            basepage.attach_save_screenshot("TC05_User_Creation_Success")
            success_text = adminpage.get_success_message()

            logger.info(f"Success message displayed: {success_text}")
            assert success_text is not None, "Success toast not visible"
            assert expected_msg in success_text, "Success message mismatch"

            logger.info("New user created successfully.")
            basepage.wait_for_url(admin_url)

        # Logout Admin
        with allure.step("Logout Admin"):
            logger.info("Logging out admin user...")
            dashboardpage.perform_logout()

        # Login using NEW USER credentials
        logger.info("=== Starting New User Login Process ===")

        with allure.step("Login using Newly Created User"):
            logger.info("Navigating to Login Page...")
            loginpage.navigate_to_url(login_url)

            logger.info(f"Entering username: {new_username}")
            loginpage.enter_username(new_username)

            logger.info(f"Entering password")
            loginpage.enter_password(new_password)

            logger.info("Clicking the Login button")
            loginpage.click_login()
            basepage.attach_save_screenshot("TC05_New_User_Login_Attempt_success")

            logger.info("Waiting for Dashboard page to load...")
            basepage.wait_for_url(dashboard_url)

        # Validate Dashboard Page after new login
        with allure.step("Validate Dashboard After New User Login"):
            assert dashboardpage.is_dashboard_loaded(), "New user login failed"
            assert dashboard_url == basepage.get_current_url(), "New user login failed"
            logger.info("New user login validated successfully.")
            dashboardpage.perform_logout()

        logger.info("====== TC05: Create & Validate New User Test Completed Successfully ======")

    # ----------------------------------------- TC 06------------------------------------------
    # Validate newly created user in search area

    @allure.title("TC06 – Validate newly created user appears in search results")
    @allure.description(
        "This test validates that a newly created user is successfully displayed when searched in the User List table."
    )
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.parametrize("row,username,password", excel_row_valid)
    def test_tc06_validate_new_user_in_search(self, setup, row, username, password):

        driver = setup
        basepage = Base_Page(driver)
        adminpage=Admin_Page(driver)
        loginpage = Login_Page(driver)
        dashboardpage=Dashboard_Page(driver)

        # config data
        login_url = get_config("Login_Orange", "url")
        dashboard_url = get_config("Dashboard_Page", "url")
        new_username = get_config("Add_new_user", "new_username")

        logger.info("========== TC06 Validate Newly Created User Search STARTED ==========")

        # LOGIN STEPS
        logger.info("=== Starting Login Process ===")

        with allure.step("Login to OrangeHRM"):
            loginpage.navigate_to_url(login_url)

            logger.info(f"Entering username: {username}")
            loginpage.enter_username(username)

            logger.info(f"Entering password")
            loginpage.enter_password(password)

            logger.info("Clicking the Login button")
            loginpage.click_login()

            logger.info("Waiting for Dashboard page to load...")
            basepage.wait_for_url(dashboard_url)

            logger.info("Logged in as Admin.")

        # Navigate to User Management
        with allure.step("navigate to admin--users tab"):
            adminpage.open_admin_menu()
            logger.info("Navigated to Admin > User Management > Users")


        # Search for the newly created user
        with allure.step(f"Search for newly created user: {username}"):
            logger.info(f"Searching for user: {new_username}")
            adminpage.search_user(new_username)
            logger.info("Search initiated.")

        # Validate user in search results
        with allure.step("Validate user appears in search results"):
            logger.info("Validating if user exists in the search results table...")
            user_present = adminpage.is_user_present_in_table(new_username)

            basepage.attach_save_screenshot("TC_06_User_Validation_Success")

            assert user_present, f"User '{new_username}' not found in table"

            logger.info(f"User '{new_username}' found successfully!")
            dashboardpage.perform_logout()

            logger.info("========== TC06 COMPLETED ==========")

    # ------------------------------------------------ TC-10 -------------------------------------------------------
    # TC-10 Claim validation

    @allure.title("TC-10: Initiate a claim request")
    @allure.description(
        "Employee initiates a new claim request, adds expense, submits the claim and validates the claim in history.")
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_tc10_initiate_claim_request(self, setup):

        driver=setup
        claimpage = Claim_Page(driver)
        basepage=Base_Page(driver)

        # ---- Test Data from config.ini ----
        login_url = get_config("Login_Orange", "url")
        dashboard_url = get_config("Dashboard_Page", "url")
        emp_username = get_config("claim", "emp_username")
        emp_password = get_config("claim", "emp_password")
        claim_type = get_config("claim", "claim_type")
        currency = get_config("claim", "currency")
        reason = get_config("claim", "reason")
        date = get_config("claim", "date")  # YYYY-MM-DD
        amount = get_config("claim", "amount")
        expected_msg = get_config("claim", "success_message")

        # LOGIN STEP
        with allure.step("Login to HRM Application"):
            logger.info("=== Starting Login Process ===")

            loginpage = Login_Page(driver)
            loginpage.navigate_to_url(login_url)

            logger.info(f"Entering username: {emp_username}")
            loginpage.enter_username(emp_username)

            logger.info(f"Entering password")
            loginpage.enter_password(emp_password)

            logger.info("Clicking the Login button")
            loginpage.click_login()

            # Wait until Dashboard URL loads
            logger.info("Waiting for Dashboard page to load...")
            basepage.wait_for_url(dashboard_url)

            logger.info("Logged in as Employee.")

        # NAVIGATE TO CLAIM SECTION
        with allure.step("Navigate to Claim Section"):
            logger.info("Opening Claim Section")
            claimpage.open_claim_section()

        # CREATE INITIAL CLAIM
        with allure.step("Create new claim request"):
            logger.info(f"Selecting claim type: {claim_type}")
            claimpage.select_claim_type(claim_type)

            logger.info(f"Selecting currency: {currency}")
            claimpage.select_currency_type(currency)

            logger.info(f"Entering reason: {reason}")
            claimpage.enter_remarks(reason)

            claimpage.create_submit_claim()

            # Validate claim success
            success_text = claimpage.get_success_message()
            logger.info("Success message received: " + success_text)

            assert success_text is not None, "Success toast not visible"
            assert expected_msg in success_text, "Claim creation success message mismatch"

        # ADD EXPENSE UNDER CLAIM
        with allure.step("Add Expense Under Claim"):
            logger.info("Adding Expense")
            claimpage.add_expense()

            logger.info(f"Selecting claim type: {claim_type}")
            claimpage.select_claim_type(claim_type)

            logger.info(f"Selecting claim date: {date}")
            claimpage.select_claim_date(date)

            logger.info(f"Entering amount: {amount}")
            claimpage.enter_amount(amount)

            logger.info(f"Entering reason/notes: {reason}")
            claimpage.enter_notes(reason)


            claimpage.click_submit_claim()

            # Validate success
            success_text_1 = claimpage.get_success_message()
            logger.info("Success message received: " + success_text)

            assert success_text_1 is not None, "Success toast not visible"
            assert expected_msg in success_text, "Expense submission success message mismatch"

        # VERIFY CLAIM IN HISTORY
        with allure.step("Validate claim in claim history"):
            logger.info("Navigating to Claim History")
            claimpage.navigate_to_claim_history()

            logger.info("Verifying claim is present in history...")
            result = claimpage.verify_claim_in_history(claim_type, currency)
            assert result is True, "claim not found in history"
            basepage.attach_save_screenshot("TC10_Claim_Validation_Success")

            logger.info("=== TC10 Claim Initiation and History Validation Completed Successfully ===")

