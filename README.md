# **Automation Testing of HR Management Web Application**

## **Project Title**

Automated Testing of the Web Application: https://opensource-demo.orangehrmlive.com

## **Project Objective**

The objective of this project is to automate the testing of the OrangeHRM HR Management demo application by simulating user interactions 
and validating core functionalities. The automation ensures that key modules like login, menu accessibility, user management, 
leave assignment, claims, and logout perform correctly. The tests are executed using structured test scripts, data-driven approaches, 
and reusable components.

## **Table of Contents:**
* Scope of the Project
* Test Suite Overview
* Tools & Technologies Used
* Page Object Model (POM) – Pages & Page Classes
* Project Structure
* Setup and Installation
* Running Tests

## **Scope of the Project**
* Automate real-world user actions such as:
  - Login & Logout
  - Menu navigation
  - User creation & validation
  - leave creation
  - Claim initiation
* Developed using **pytest** and **Selenium**
* Page Object Model (POM)
* Included both positive and negative test scenarios.
* Used explicit waits to synchronize UI actions.
* Performed cross-browser testing.
* Integrated data-driven testing using Excel and config files
* Logging using Python `logging` module
* Reports generated using allure and html
* Runs test through pytest

## **Test Suite Overview**

Below are the detailed test cases automated in this project.
      - Test_Login_Page_OrangeHRM.py
      - Test_Dashboard_Page_OrangeHRM.py

### **Test_Login_Page_OrangeHRM.py**
    - Test Case 2 – Verify Home URL Accessibility
    - Test Case 3 – Validate Login Field Presence
    - Test Case 1 – Validate Login Using Multiple Credentials
    - Test Case 7 – Verify "Forgot Password" Functionality

### **Test_Dashboard_Page_OrangeHRM.py**
    - Test Case 4 – Verify Menu Items After Login
    - Test Case 8 – Validate “My Info” Sub-Menu Items
    - Test Case 9 – Assign Leave and Verify Assignment
    - Test Case 5 – Create a New User & Validate Login
    - Test Case 6 – Validate New User in User List
    - Test Case 10 – Initiate a Claim Request

**Test Case 1 – Validate Login Using Multiple Credentials**

**Scenario:** Test login with different username/password combinations (Data-Driven Testing).
**Steps:**
* Load datasets from Excel.
* Attempt login for each set.
* Validate success or failure.
* For successful login, perform logout.
* For unsuccessful login, validate error messages.
  
**Expected Result:**
* Valid credentials → Login successful.
* Invalid credentials → Appropriate error message displayed.
* Login status validated.

**Test Case 2 – Verify Home URL Accessibility**

**Scenario:** Ensure the site loads correctly.
**Steps:**
* Launch browser.
* Navigate to OrangeHRM URL.
  
**Expected Result:**
* Home page loads without error.

**Test Case 3 – Validate Login Field Presence**

**Scenario**: Verify Username and Password login fields.

**Expected Result:**
Username and Password fields are visible and enabled.

**Test Case 4 – Verify Menu Items After Login**

**Scenario:** Ensure main menu navigation is working.
Menu items: Admin, PIM, Leave, Time, Recruitment, My Info, Performance, Dashboard.

**Expected Result**:
All menu items visible and clickable.

**Test Case 5 – Create a New User & Validate Login**

**Scenario:** Add a new user in admin page and log in with the same.
**Steps:**
* Open Admin module.
* Create a new user.
* Log out admin.
* Login with new user credentials.
  
**Expected Result:**
* User is created successfully.
* New user can log in.

**Test Case 6 – Validate New User in User List**

**Scenario:** Verify user creation in the admin section.

**Expected Result:**
Newly created user appears in User Management → User List.

**Test Case 7 – Verify "Forgot Password" Functionality**

**Scenario:** Test reset password flow.

**Expected Result:**
* Confirmation message is displayed.
* User is redirected correctly.

**Test Case 8 – Validate “My Info” Sub-Menu Items**

**Scenario:** Ensure all personal information sections are accessible.

**Expected Result:**
Sub-menu items such as Personal Details, Contact Details, Emergency Contacts, etc. are visible and clickable.

**Test Case 9 – Assign Leave and Verify Assignment**

**Scenario:** Test leave assignment functionality.

**Expected Result:**
* Leave assigned successfully.
* Success message displayed.
* Leave reflects in employee leave records.

**Test Case 10 – Initiate a Claim Request**

**Scenario:** Submit a new claim.

**Expected Result:**
* Claim submitted successfully.
* Confirmation message displayed.
* Claim listed in user’s claim history.

## Tools & Technologies Used

**Programming Language:** Python 

**Testing Framework:** Pytest

**Automation Tool:** Selenium WebDriver

**Design Pattern:** Page Object Model (POM)

**Data Handling:** Excel(DDT) (e.g.OpenPyXL)

**Reporting:** Allure and HTML Reports

**Browsers Tested:** Chrome, Edge, Firefox

## **Page Object Model (POM) – Pages & Page Classes**
Each page of the OrangeHRM application is represented using a Page Object Class. These classes contain:
* Locators
* Page actions (methods)
* Reusable functions for interaction

### **Pages Included in the Project:**
**1. Login Page (login_page.py)**
Contains methods for:
* Entering username
* Entering password
* Clicking login button
* Handling invalid login messages

**2. Admin Page (admin_page.py)**
Methods include:
* Navigating to User Management
* Adding new users
* Searching for users
* Validating user presence in the table

**3. Dashboard Page (dashboard_page.py)**
Handles:
* Menu verification (Admin, PIM, Leave, etc.)
* Checking visibility & clickability of options

**4. My Info Page (myinfo_page.py)**
Contains actions for:
* Navigating to Personal Details
* Contact Details
* Emergency Contacts
* Validating each sub-menu page

**5. Leave Page (leave_page.py)**
Handles:
* Navigating to Assign Leave
* Selecting leave type
* Filling employee name
* Submitting leave assignment
* Validating leave success message

**6. Claim Page (claim_page.py)**
Methods include:
* Navigating to Claims section
* Initiating claim request
* Selecting claim type
* Entering amount & reason
* Submitting claim form
* Validating confirmation

**7. Base Page (base_page.py)**
A reusable foundation class that includes:
* Wait functions (Explicit waits)
* Click actions
* Send keys actions
* Common utility methods

## **Project Structure:**

Project2_OrangehrmHrm_Automation/                             ← Root folder containing entire automation framework

│

├── .venv/                                                    ← Virtual environment for Python dependencies

│

├── locators/                                                 ← Centralized file for storing all element locators

│ └── locators.py                                             ← Contains XPaths, CSS selectors, IDs used across pages

│

├── pages/                                                    ← Page Object Model classes (each file = one application page)

│ ├── admin_page.py                                           ← Admin module actions (Add/Search users)

│ ├── base_page.py                                            ← Base class with common functions (waits, clicks, inputs)

│ ├── claim_page.py                                           ← Claim initiation workflow methods

│ ├── dashboard_page.py                                       ← Main menu verification & navigation

│ ├── leave_assign_page.py                                    ← Assign Leave page elements & actions

│ ├── login_page.py                                           ← Login page interactions

│ └── myinfo_page.py                                          ← "My Info" module navigation & validations

│

├── Reports/                                                  ← Stores HTML/Allure execution reports

│ ├── html                                                    ← Stores HTML execution reports

│ └── allure                                                  ← Stores Allure execution reports

│

├── screenshots/                                              ← Captures screenshots on success and failure

│
├── testdata/                                                 ← External test data files

│ └── test_data.xlsx                                          ← Data-driven test credentials & inputs

│

├── tests/                                                   ← Pytest test scripts for all modules

│ ├── Test_Dashboard_Page_OrangeHRM.py                      ← Dashboard & menu tests

│ └── Test_Login_Page_OrangeHRM.py                          ← Login module test cases

│

├── utility/                                                ← Helper utilities (config, Excel reader)

│ ├── config_write.py                                       ← Writes/updates values inside config.ini

│ ├── config_reader.py                                      ← Reads configuration values (URL, browser, credentials)

│ └──excel_reader.py                                        ← Reads test data from Excel (DDT support)

│

├── .gitignore                                              ← Git ignore rules

├── config.ini                                              ← Environment/configuration settings

├── conftest.py                                             ← Pytest fixtures (browser setup, loggers)

├── pytest.ini                                              ← Pytest markers & test settings

├── README.md                                               ← Project documentation

├── requirements.txt                                        ← List of required Python packages

└── test_logs.log                                           ← Execution logs

## **Setup and Installation**
To set up and run this project locally, follow these steps:

#### **Clone the Repository:**
git clone https://github.com/Poornima91-pg/Project2_Orange_HR_Management_Automation.git
cd Project2_OrangehrmHrm_Automation

#### **Install Dependencies:**
pip install -r requirements.txt

#### **Set Up Environment Variables:**

Create a config.ini file in the project root to store environment data like credentials and browser.
(eg)
[browser_name]

browser = chrome

username=*****

password=*****

## **Running Tests**
To execute tests, use the following commands:

**Run All Tests with default browser(chrome) in config.ini file and displayed result on console:**

change to required browser name in configwrite.py file and run it then run the below command

 pytest -v -s 

**Run All Tests with browser passed through command line and displayed result on console:**

 pytest -v --browser-name firefox

**Run a Single Test File**

 pytest Test_Dashboard_Page_OrangeHRM.py::<Testcase name>
 
 pytest -k <Testcase name> 

**Run All Tests and  generate html report**

Generate HTML Report:

pytest --html=report.html -v -s

**Run All Tests and  generate allure report**

* Generate Allure Results:
  
pytest --alluredir=reports/allure-results

* Create Allure Report:
  
allure generate reports/allure-results -o reports/allure-report --clean

* Open Allure Report:
  
allure open reports/allure-report

#### **Logs & Reports**
* Logs are stored in test_logs.log
  Logs include:
    * Test start and end
    * Steps inside each page
    * Errors and failures
    * Browser/driver events
* Reports are stored in reports folder
* Screenshots for failed/passed tests are saved inside the screenshots/ directory.

#### **DDT (Data Driven Testing)**
* Login data from Excel
* User creation data from Excel
* Utils: excel_reader.py

### **Conclusion**
This project provides a complete Selenium-Python automation suite using industry-level frameworks like 
POM, DDT, Pytest, Allure, and logs. It ensures a reliable and maintainable automation setup for OrangeHRM.

