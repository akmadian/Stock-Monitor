# Stockmonitor
My personal stock monitor project
Python Version - 3.6
Dependencies:
 - lxml
 - requests
 - matplotlib
 - smtplib
 - twilio
 - numpy
 
 
main.py
 - Main script.
 
*_xpaths.csv
 - CSV File containing XPATH for each value to be scraped.
 
COMM_LONGTERM.csv
 - Contains long term data about each stock. 
 
 
 
main_config.ini
Config file for main.py, contains information used for bug reporting and scraping
Module dependencies are listed by prefix in the file but they're also listed here.
Fields can be left blank if you don't want to use that service. Handling for blank fields
 is built in.

All fields expect plaintext with no additional formatting for the interpreter.
larloginemail = The email to be used to log in to gmail for email reporting.
larloginpassword = The password for larloginemail.
lartoemail = The email reports will be sent to.
twilioaccssid = The ssid for your twilio account
twilioauthtoken = The authtoken for your twilio account.
twiliosendnum = The number that twilio reports will be sent from, your twilio account number.
twiliorecievenum = The number that twilio reports will be sent to.

website = The website to scrape values from
header = The header to use for the requests.get() call in scrape
 
