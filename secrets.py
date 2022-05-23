import time

from scrape import login_delay

# Step 0: Input your tesla account details
tesla_account_email = "YOUR TESLA EMAIL HERE"
tesla_account_password = "YOUR TESLA PASSWORD HERE"

def tesla_login(driver):
  driver.get("https://tesla.com/teslaaccount")
  driver.find_element_by_css_selector("#form-input-identity").send_keys(tesla_account_email)
  time.sleep(2)
  driver.find_element_by_css_selector("#form-submit-continue").click()
  time.sleep(2)
  driver.find_element_by_css_selector("#form-input-credential").send_keys(tesla_account_password)
  time.sleep(2)
  driver.find_element_by_css_selector("#form-submit-continue").click()

  return driver
  