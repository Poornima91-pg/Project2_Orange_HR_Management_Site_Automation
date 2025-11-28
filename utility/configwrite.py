from configparser import ConfigParser

"""
create_config.py

This module generates a configuration file (config.ini) for automating tests on the GUVI web application.
It stores test data and environment details like browser name, URLs, login credentials, and expected titles.
The config file is used throughout the automation framework to achieve maintainability and reusability.
"""

def create_config():
    """
        Creates a configuration file 'config.ini' with sections for:
        - browser configuration
        - login page details
        - Excel details
        - Dashboard page details
        - Menu URL details
        - Add User details
        - Password reset details
        - My Info URL details
        - Leave details
        - claim details
        """

    # Create a ConfigParser object to write config data
    config = ConfigParser()

    # Browser configuration
    config["browser_name"]= {
        # browser options: chrome, firefox, edge
        "browser":"chrome"
    }

    # Login page details
    config["Login_Orange"] = {
        "url": "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"

    }

    # Excel details
    config["Excel"] = {
        "path": "testdata/test_data.xlsx",
        "sheet": "test_data",
        "tester": "Poornima"
    }

    # Dashboard page details
    config["Dashboard_Page"]={
        "url":"https://opensource-demo.orangehrmlive.com/web/index.php/dashboard/index"
    }

    # Menu URL details
    config["Menu_URLs"]={
        "Admin":"https://opensource-demo.orangehrmlive.com/web/index.php/admin/viewSystemUsers",
        "PIM":"https://opensource-demo.orangehrmlive.com/web/index.php/pim/viewEmployeeList",
        "Leave":"https://opensource-demo.orangehrmlive.com/web/index.php/leave/viewLeaveList",
        "Time":"https://opensource-demo.orangehrmlive.com/web/index.php/time/viewEmployeeTimesheet",
        "Recruitment":"https://opensource-demo.orangehrmlive.com/web/index.php/recruitment/viewCandidates",
        "MyInfo":"https://opensource-demo.orangehrmlive.com/web/index.php/pim/viewPersonalDetails/empNumber/7",
        "Performance":"https://opensource-demo.orangehrmlive.com/web/index.php/performance/searchEvaluatePerformanceReview",
        "Dashboard":"https://opensource-demo.orangehrmlive.com/web/index.php/dashboard/index"
    }

    # Add User details
    config["Add_new_user"]= {
        "new_username":"Test0981",
        "new_password":"Test@345",
        "emp_name":"Orange Test",
        "role":"ESS", # Admin or ESS
        "status":"Enabled",
        "admin_url":"https://opensource-demo.orangehrmlive.com/web/index.php/admin/viewSystemUsers",
        "add_url":"https://opensource-demo.orangehrmlive.com/web/index.php/admin/saveSystemUser",
        "success_message": "Successfully Saved"
    }

    # Password reset details
    config["Reset"]={
        "url":"https://opensource-demo.orangehrmlive.com/web/index.php/auth/sendPasswordReset",
        "username":"Testused09",
        "success_message":"Reset Password link sent successfully"
    }

    # My Info URL details
    config["MYINFO_URLS"] = {
        "personal_details": "https://opensource-demo.orangehrmlive.com/web/index.php/pim/viewPersonalDetails/empNumber/7",
        "contact_details": "https://opensource-demo.orangehrmlive.com/web/index.php/pim/contactDetails/empNumber/7",
        "emergency_contacts": "https://opensource-demo.orangehrmlive.com/web/index.php/pim/viewEmergencyContacts/empNumber/7",
        "dependents": "https://opensource-demo.orangehrmlive.com/web/index.php/pim/viewDependents/empNumber/7",
        "immigration": "https://opensource-demo.orangehrmlive.com/web/index.php/pim/viewImmigration/empNumber/7",
        "job": "https://opensource-demo.orangehrmlive.com/web/index.php/pim/viewJobDetails/empNumber/7",
        "salary": "https://opensource-demo.orangehrmlive.com/web/index.php/pim/viewSalaryList/empNumber/7",
        "report_to": "https://opensource-demo.orangehrmlive.com/web/index.php/pim/viewReportToDetails/empNumber/7",
        "qualifications": "https://opensource-demo.orangehrmlive.com/web/index.php/pim/viewQualifications/empNumber/7",
        "memberships": "https://opensource-demo.orangehrmlive.com/web/index.php/pim/viewMemberships/empNumber/7"
    }

    # Leave details
    config["Leave_Data"] = {
        "employee_name": "Orange Test",
        "leave_type": "CAN - Personal",
        "from_date": "2025-12-15",
        "to_date": "2025-12-15",
        "comments": "Annual leave assigned automatically",
        "success_message": "Successfully Saved",
        "search_message" :"No Records Found"
    }

    # claim details
    config["claim"]={
        "emp_username":"Test0981",
        "emp_password":"Test@345",
        "claim_type":"Accommodation",
        "currency":"Indian Rupee",
        "reason":"hotel stay",
        "date":"2025-11-19",
        "amount":"5000",
        "success_message": "Success"
    }

    # Write the configuration data to config.ini file
    with open("../config.ini", "w") as configfile:
        config.write(configfile)

if __name__ == "__main__":
    create_config()



