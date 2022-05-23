# Tesla Service Manual Scraper

This script will download the Tesla Service Manual onto a local doc folder for offline access.  This is geared for Windows only.

## Setup

1. Go into `secrets.py` and fill out `tesla_account_email` and `tesla_account_password` with your account and password.
2. Go into `scrape.py` and enter the index URL of the manual you want saved by changing `service_manual_index` and `base_url` variables.  It is defaulted to the Model 3.
3. If you have 2FA or other challenges with login, consider changing `login_delay` to 2 or 3 seconds so you can manually enter your credentials.
4. Setup Python 3.  See tutorial at: <https://wiki.python.org/moin/BeginnersGuide/Download>
5. Setup selenium for Python.  To use the required stealth module, you **must** use the Chromium webdriver.  See tutorial at: <https://blog.testproject.io/2019/07/16/installing-selenium-webdriver-using-python-chrome/>
6. Pip install the required packages (including `requests`, `selenium`, `selenium-stealth`, and `beautifulsoup4`).  On windows, you run the following commands on command prompt (CMD):
    1.  `cd C:\Users\Anson\Desktop\TeslaServiceManualScraper` [template, the path should go wherever you saved this readme]
    2.  `run pip install -r requirements.txt`
7. Run `scrape.py` by typing `python scrape.py`

## Viewing offline

### Option 1: Easy Way

1. Go into `docs/` folder and open up `index.html`.  You're going to get 99% of the service manual just like that, but no search functionality.

### Option 2: HTTP Server (thanks to TheNexusAvenger)

1. Run CMD on Windows, and change the directory to the `docs` folder.  Something like this `cd C:\Users\Anson\Desktop\TeslaServiceManualScraper`
2. Run the following command: `python -m http.server` (Python obviously needs to be installed)
3. Use a web browser and navigate to: `http://localhost:8000/` to see the full service manual including search.

## Tips

* A full scrape of the Model 3 service manual **took over 30 minutes**.  This script is set up so that you can stop the script, and then continue later on.
* Keep an eye out, Tesla's website seems to boot you out of logged in status after about 250 pages or 20 minutes of continuous refreshing.  So it might be worthwhile to run this on the side while keeping an eye on your login status.
* Total file size of the Model 3 service manual is roughly **2.2GB**.
* This script can likely be modified for MacOS easily, but I'm not familiar with how to install Selenium and chromedriver on MacOS.  See issues below  **Windows only for now.**
