# **Automation Testing of HR Management Web Application**

## **Project Title**

Automated Testing of the Web Application: https://opensource-demo.orangehrmlive.com

## **Project Objective**

The objective of this project is to automate the testing of the OrangeHRM HR Management demo application by simulating user interactions 
and validating core functionalities. The automation ensures that key modules like login, menu accessibility, user management, 
leave assignment, claims, and logout perform correctly. The tests are executed using structured test scripts, data-driven approaches, 
and reusable components.

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

### **Test_Login_Page_OrangeHRM.py**
