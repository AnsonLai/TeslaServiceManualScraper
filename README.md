# Tesla Service Manual Scraper

This script will download the Tesla Service Manual onto a local doc folder for offline access.

## Setup

1. Go into `secrets.py` and fill out `tesla_account_email` and `tesla_account_password` with your account and password.
2. Go into `scrape.py` and enter the index URL of the manual you want saved.  It is defaulted to the Model 3.
3. Setup selenium for Python.  To use the required stealth module, you must use the Chromium webdriver.  See tutorial at: <https://blog.testproject.io/2019/07/16/installing-selenium-webdriver-using-python-chrome/>
4. Pip download the required packages including:
  1. `selenium-stealth`
  2. `beautifulsoup4`
5. Run `scrape.py`

## Tips

* A full scrape of the Model 3 service manual **took over 30 minutes**.  This script is set up so that you can stop the script, and then continue later on.
* Keep an eye out, Tesla's website seems to boot you out of logged in status after about 250 pages or 20 minutes.  So it might be worthwhile to run this on the side while keeping an eye on your login status.
* Total file size of the Model 3 service manual is roughly **2.2GB**.
* There is minimal styling applied on the service manual.  This script does not download those files.  If you want the full experience, you should download the following folders (seen in your browser's developer tools, under the Sources tab):
  * css
  * design-system
  * img
  * js
    * *This one is useful, they use jQuery*