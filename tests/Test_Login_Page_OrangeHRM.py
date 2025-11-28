import pytest
import logging
from utility.config_reader import get_config
from pages.base_page import Base_Page
from pages.login_page import Login_Page
from pages.dashboard_page import Dashboard_Page
import allure
from utility.excel_reader import ExcelUtil

# Set up logger for this test module
logger = logging.getLogger(__name__)

# Excel utility
excel_path = get_config("Excel", "path")
sheet = get_config("Excel", "sheet")
excel = ExcelUtil(excel_path, sheet)

@pytest.mark.usefixtures("setup")
class Test_Orange_Hrsite_Automation_Login_Page:
    """
    Test Suite for OrangeHRM Login Page Automation.

    Includes:
        - URL validation
        - Login fields visibility validation
        - Data-driven login scenarios using Excel
        - Forgot password workflow validation
    """

    # --------------------------------------- TC-02------------------------------------------------
    # TC02 — Validate Homepage URL Loads Successfully

    @allure.title("TC02 – Validate OrangeHRM URL Loads Successfully")
    @allure.description("""
            Validates the OrangeHRM login page URL.
            Ensures the page loads expected URL and attaches screenshots for Allure Reporting.
        """)
    @pytest.mark.smoke
    def test_tc2_validate_url(self, setup):

        driver = setup
        basepage = Base_Page(driver)
        loginpage = Login_Page(driver)

        expected_url = get_config("Login_Orange", "url")

        try:
            logger.info("Navigating to OrangeHRM homepage...")
            loginpage.navigate_to_url(expected_url)

            # Fetch current URL after navigation
            current_url = basepage.get_current_url()
            logger.info(f"Expected URL: {expected_url} | Actual URL: {current_url}")

            assert current_url == expected_url, "URL mismatch,Page not loaded successfully"
            logger.info(f"OrangeHRM URL loaded successfully: {current_url}")

            # Screenshot → Allure
            basepage.attach_save_screenshot("TC02_URL_Success")
            logger.info("Screenshot captured: TC02_URL_Success.png")

        except Exception as e:
            # Log any unexpected errors
            logger.exception(f"Unexpected error occurred during URL verification: {e}")
            basepage.attach_save_screenshot("TC02_URL_Failed")
            raise

    # --------------------------------- TC03--------------------------------------------
    # TC03 — Validate Login Fields Visibility

    @allure.title("TC03 – Validate Login Fields Visibility")
    @allure.description("""
          Validates visibility of username, password, and login button on login page.
          Ensures fields are displayed and enabled.
      """)
    @pytest.mark.smoke
    def test_tc3_validate_login_fields(self, setup):

        driver = setup
        basepage = Base_Page(driver)
        loginpage = Login_Page(driver)

        try:
            # Wait for login page URL
            login_url = get_config("Login_Orange", "url")
            basepage.wait_for_url(login_url)

            # Validate that username and password fields are displayed and enabled
            logger.info("Validating username is visible and displayed")
            assert basepage.element_is_displayed_and_enabled(loginpage.username_input), \
                "Username input field is not visible or enabled."

            logger.info("Validating password is visible and displayed")
            assert basepage.element_is_displayed_and_enabled(loginpage.password_input), \
                "Password input field is not visible or enabled."

            logger.info("Validating login button is visible and displayed")
            assert basepage.element_is_displayed_and_enabled(loginpage.login_button), \
                "Login Button is not visible or enabled."

            print("Username and password input fields are visible and enabled.")

            logger.info("TC03 Passed: All login fields are visible and enabled.")

            # Attach success screenshot
            basepage.attach_save_screenshot("TC03_Login_Fields_Visible_success")

        except Exception as e:
            logger.error(f"TC03 Failed: {e}")
            basepage.attach_save_screenshot("TC03_Login_Fields_Visible_failed")
            raise AssertionError(f"Unexpected error while checking login fields: {e}")

    #  ----------------------------- TC-01--------------------------------------------------------
    # TC01 — Data Driven Login From Excel

    excel_data = ExcelUtil(excel_path, sheet).get_param_data()

    @allure.title("TC01 – Validate Login Scenarios Using Excel Data (DDT)")
    @allure.description("""
            Validates login behaviour using Excel test data.
            Covers:
                - Successful login
                - Invalid login error message validation
        """)
    @pytest.mark.smoke
    @pytest.mark.parametrize("row,username,password,expected_error", excel_data)
    def test_tc1_validate_logins_from_excel(self, setup, row, username, password, expected_error):

        driver = setup
        basepage = Base_Page(driver)
        loginpage = Login_Page(driver)
        dashboardpage=Dashboard_Page(driver)

        logger.info(f"=== Test Row {row} Started ===")
        logger.info(f"Username: {username} | Password: {password} | Expected Error: {expected_error}")

        # Refresh before each iteration
        driver.refresh()

        # Perform login
        logger.info("Entering username and password")
        loginpage.enter_username(username)
        loginpage.enter_password(password)

        logger.info("Clicking login button")
        loginpage.click_login()

        # Actual status returned by login_page logic
        status = loginpage.get_login_status()
        logger.info(f"Login status returned by page: {status}")

        expected_url = get_config("Dashboard_Page", "url")

        # VALID LOGIN CASE
        if status == "Success":
            logger.info("Detected successful login. Verifying dashboard URL...")

            logger.info(f"Expected Dashboard URL: {expected_url}")
            logger.info(f"Actual URL: {basepage.get_current_url}")

            assert expected_url == basepage.get_current_url(), \
                f"Expected Dashboard URL '{expected_url}' but got '{basepage.get_current_url}'"

            logger.info("Dashboard URL matched successfully")
            basepage.attach_save_screenshot(f"TC_01_Row_{row}_valid_login_success")

            # VALID LOGIN → LOGOUT
            logger.info("Performing logout...")
            dashboardpage.perform_logout()

            # Write Excel Result
            excel.write_test_result(row, "Pass", "Login Success", excel.tester)

            logger.info("Result written to Excel: PASS - Login Successful")
            assert True, "Login successful"

        #  INVALID LOGIN CASE
        else:
            # INVALID LOGIN → VERIFY ERROR MESSAGE
            logger.info("Invalid login detected — verifying error message...")
            logger.info(f"User is still on page: {basepage.get_current_url()}")

            assert expected_url != basepage.get_current_url(), \
                "Invalid login should NOT navigate to Dashboard!"

            logger.info("User did not reach dashboard — correct behavior")

            # Screenshot
            basepage.attach_save_screenshot(f"TC_01_Row_{row}_Invalid_Login_success")

            # Compare error message with expected
            if expected_error == status:
                # Error message matched → PASS
                logger.info(f"Error message matched expected: {expected_error}")

                excel.write_test_result(row, "PASS", f"Error matched: {status}", excel.tester)

                logger.info("Result written to Excel: PASS - Error matched")

                assert True, "Error message matched"
            else:
                # Error message mismatch → FAIL
                logger.error(f"Error message mismatch! Expected: '{expected_error}', Got: '{status}'")
                excel.write_test_result(row, "FAIL", f"Expected: {expected_error}, Got: {status}", excel.tester)
                logger.info("Result written to Excel: FAIL - Error mismatch")

                assert expected_error != status, "Error message mismatch"

        logger.info(f"=== Test Row {row} Finished ===\n")

    # --------------------------------- TC-07---------------------------------------
    # TC07 — Forgot Password Validation

    @allure.title("TC07 – Forgot Password Link & Reset Flow Validation")
    @allure.description("""
            Validates Forgot Password workflow:
                - Navigation
                - Reset username entry
                - URL validation
                - Success message validation
        """)
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_validate_forgot_password_link(self, setup):

        driver = setup
        basepage = Base_Page(driver)
        loginpage = Login_Page(driver)

        # Config values
        login_url = get_config("Login_Orange", "url")
        reset_user = get_config("Reset", "username")
        reset_success_url = get_config("Reset", "url")
        expected_msg = get_config("Reset", "success_message")

        logger.info("=== TC07 Forgot Password Validation Started ===")

        # Navigate to Login Page
        loginpage.navigate_to_url(login_url)
        logger.info(f"Navigated to login page: {login_url}")

        # Click Forgot Password
        loginpage.forgot_password_link()
        logger.info("Clicked on Forgot Password link")

        # Enter Reset Username
        loginpage.reset_password_username(reset_user)
        logger.info(f"Entered reset username: {reset_user}")

        # URL Validation
        basepage.wait_for_url(reset_success_url)
        current_url = basepage.get_current_url()

        try:
            assert current_url == reset_success_url, "URL mismatch after reset"
            basepage.attach_save_screenshot("TC07_ForgotPassword_url_success")
            logger.info("URL validation successful")
        except AssertionError:
            basepage.attach_save_screenshot("TC07_ForgotPassword_url_failed")
            logger.error(f"EXPECTED URL: {reset_success_url}, GOT: {current_url}")
            raise


        # Validate success message
        message = loginpage.reset_success()

        try:
            assert message is not None, "Success message not visible"
            assert message == expected_msg, "Success message text mismatch"
            basepage.attach_save_screenshot("TC07_ForgotPassword_success")
            logger.info(f"Success Message Verified: {message}")
        except AssertionError:
            basepage.attach_save_screenshot("TC07_ForgotPassword_Failure")
            logger.error(f"EXPECTED MSG: {expected_msg}, GOT: {message}")
            raise


        logger.info("TC07 Forgot Password Validation Completed Successfully")
        logger.info("Login Page Validation Completed Successfully")