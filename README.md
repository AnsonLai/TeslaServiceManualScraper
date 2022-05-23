# Tesla Service Manual Scraper

This script will download the Tesla Service Manual onto a local doc folder for offline access.  This is geared for Windows only.

## Setup

1. Go into `secrets.py` and fill out `tesla_account_email` and `tesla_account_password` with your account and password.
2. Go into `scrape.py` and enter the index URL of the manual you want saved.  It is defaulted to the Model 3.
3. Setup Python 3.  See tutorial at: <https://wiki.python.org/moin/BeginnersGuide/Download>
4. Setup selenium for Python.  To use the required stealth module, you **must** use the Chromium webdriver.  See tutorial at: <https://blog.testproject.io/2019/07/16/installing-selenium-webdriver-using-python-chrome/>
5. Pip install the required packages (including `requests`, `selenium`, `selenium-stealth`, and `beautifulsoup4`).  On windows, you run the following commands on command prompt (CMD):
  1.  `cd C:\Users\Anson\Desktop\TeslaServiceManualScraper` [template, the path should go wherever you saved this readme]
  2.  `run pip install -r requirements.txt`
6. Run `scrape.py` by typing `python scrape.py`

## Tips

* A full scrape of the Model 3 service manual **took over 30 minutes**.  This script is set up so that you can stop the script, and then continue later on.
* Keep an eye out, Tesla's website seems to boot you out of logged in status after about 250 pages or 20 minutes.  So it might be worthwhile to run this on the side while keeping an eye on your login status.
* Total file size of the Model 3 service manual is roughly **2.2GB**.
* There is minimal styling applied on the service manual.  This script does not download those files.  If you want the full experience, you should download the following folders (seen in your browser's developer tools, under the Sources tab).  The JS folder is probably the most helpful.
  * css/
    * custom.css
  * design-system/
    * 5.4.1/
      * index.css
      * index.js
  * img/
    * spritemap.svg
  * js/
    * vendor/
      * jquery.magnific-popup.min.js
      * jquery-3.5.1.min.js
      * lunr.js
    * search.js
* This script can likely be modified for MacOS easily, but I'm not familiar with how to install Selenium and chromedriver on MacOS.  **Windows only for now.**
