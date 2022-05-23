from selenium import webdriver
from selenium_stealth import stealth
from bs4 import BeautifulSoup
import time

import os
import requests
import pickle

from secrets import tesla_login

# Step 0: Indicate which manual you plan to scrape, currently set to Model 3.  Also increase the login delay to give yourself time to login if you have 2FA or encounter other login issues.
service_manual_index = "https://service.tesla.com/docs/Model3/ServiceManual/en-us/index.html"
base_url = "https://service.tesla.com/docs/Model3/ServiceManual/en-us/"
login_delay = 0


# Step 1: Set up the webdriver
options = webdriver.ChromeOptions()
# You can run this in headless mode, but it is not advised because Tesla might kick you out after ~250 pages or so
# options.add_argument("--headless")

options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(options=options, executable_path=r"chromedriver.exe")

stealth(driver,
  languages=["en-US", "en"],
  vendor="Google Inc.",
  platform="Win32",
  webgl_vendor="Intel Inc.",
  renderer="Intel Iris OpenGL Engine",
  fix_hairline=True,
)

# Step 2: Login to Tesla
time.sleep(login_delay)
driver = tesla_login(driver)
time.sleep(login_delay)

# Step 3: Get to the index page
driver.get(service_manual_index)
time.sleep(10)

window1 = driver.window_handles[1]
driver.switch_to.window(window1)

source = driver.find_element_by_css_selector("html").get_attribute('outerHTML')


os.makedirs(os.path.dirname('docs/index.html'), exist_ok=True)
with open('docs/index.html', 'w', encoding='utf-8') as f:
  f.write(source)

visited_urls = ['index.html']
banned_urls = []
upcoming_urls = []
img_urls = []
visited_img_urls = []

soup = BeautifulSoup(source, 'html.parser')
for link in soup.find_all('a'):
  if link.get('href') not in visited_urls and link.get('href') not in banned_urls and link.get('href') not in upcoming_urls:
    if link.get('href').startswith('GUID') and link.get('href').endswith('.html'):
      upcoming_urls.append(link.get('href'))

for img in soup.find_all('img'):
  if img.get('src') not in img_urls:
    img_urls.append(img.get('src'))

# Step 4: Get the index.json for search functionality (thanks to TheNexusAvenger!) and other assorted supporting files
headers = {
"User-Agent":
  "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
}
s = requests.session()
s.headers.update(headers)

for cookie in driver.get_cookies():
    c = {cookie['name']: cookie['value']}
    s.cookies.update(c)

r = s.get(base_url + 'index.json', allow_redirects=True)
open("docs/index.json", 'wb').write(r.content)

os.makedirs(os.path.dirname('docs/css/custom.css'), exist_ok=True)
r = s.get(base_url + 'css/custom.css', allow_redirects=True)
open("docs/css/custom.css", 'wb').write(r.content)

os.makedirs(os.path.dirname('docs/js/vendor/jquery-3.5.1.min.js'), exist_ok=True)
r = s.get(base_url + 'js/vendor/jquery-3.5.1.min.js', allow_redirects=True)
open("docs/js/vendor/jquery-3.5.1.min.js", 'wb').write(r.content)

r = s.get(base_url + 'js/vendor/jquery.magnific-popup.min.js', allow_redirects=True)
open("docs/js/vendor/jquery.magnific-popup.min.js", 'wb').write(r.content)

r = s.get(base_url + 'js/vendor/lunr.js', allow_redirects=True)
open("docs/js/vendor/lunr.js", 'wb').write(r.content)

r = s.get(base_url + 'js/search.js', allow_redirects=True)
open("docs/js/search.js", 'wb').write(r.content)

os.makedirs(os.path.dirname('docs/img/spritemap.svg'), exist_ok=True)
r = s.get(base_url + 'img/spritemap.svg', allow_redirects=True)
open("docs/img/spritemap.svg", 'wb').write(r.content)

os.makedirs(os.path.dirname('docs/design-system/5.4.1/index.css'), exist_ok=True)
r = s.get(base_url + 'design-system/5.4.1/index.css', allow_redirects=True)
open("docs/design-system/5.4.1/index.css", 'wb').write(r.content)

r = s.get(base_url + 'design-system/5.4.1/index.js', allow_redirects=True)
open("docs/design-system/5.4.1/index.js", 'wb').write(r.content)

os.makedirs(os.path.dirname('docs/tds-fonts/3.x/woff2/GothamSSm-Bold_web.woff2'), exist_ok=True)
r = s.get(base_url + 'tds-fonts/3.x/woff2/GothamSSm-Bold_web.woff2', allow_redirects=True)
open("docs/tds-fonts/3.x/woff2/GothamSSm-Bold_web.woff2", 'wb').write(r.content)

r = s.get(base_url + 'tds-fonts/3.x/woff2/GothamSSm-Book_web.woff2', allow_redirects=True)
open("docs/tds-fonts/3.x/woff2/GothamSSm-Book_web.woff2", 'wb').write(r.content)

r = s.get(base_url + 'tds-fonts/3.x/woff2/GothamSSm-Medium_web.woff2', allow_redirects=True)
open("docs/tds-fonts/3.x/woff2/GothamSSm-Medium_web.woff2", 'wb').write(r.content)

# Step 5: Set up Python pickle to save session.  You can stop the script and run it again to resume where you left off.
try:
  pickle_in = open("dict.pickle","rb")
  url_dict = pickle.load(pickle_in)
  visited_urls = url_dict['visited_urls']
  banned_urls = url_dict['banned_urls']
  upcoming_urls = url_dict['upcoming_urls']
  img_urls = url_dict['img_urls']
except:
  pickle_out = open("dict.pickle","wb")
  pickle.dump({
    'visited_urls': visited_urls,
    'banned_urls': banned_urls,
    'upcoming_urls': upcoming_urls,
    'img_urls': img_urls,
    'visited_img_urls': visited_img_urls
  }, pickle_out)
  pickle_out.close()
  print("****** SESSION SAVED ******")

# Step 6: Loop to get all the html pages, and store information about images to be downloaded later.
while upcoming_urls:
  for url in upcoming_urls:
    if len(visited_urls) % 50 == 0:
      pickle_out = open("dict.pickle","wb")
      pickle.dump({
        'visited_urls': visited_urls,
        'banned_urls': banned_urls,
        'upcoming_urls': upcoming_urls,
        'img_urls': img_urls,
        'visited_img_urls': visited_img_urls
      }, pickle_out)
      pickle_out.close()
      print("****** SESSION SAVED ******")
    if url.startswith('GUID') and url.endswith('.html'):
      driver.get(base_url + url)
    else:
      upcoming_urls.remove(url)
      continue
    source = driver.find_element_by_css_selector("html").get_attribute('outerHTML')

    with open('docs/' + url, 'w', encoding='utf-8') as f:
      f.write(source)
      visited_urls.append(url)
      upcoming_urls.remove(url)
      print("visited: " + str(len(visited_urls)))
      print("upcoming: " + str(len(upcoming_urls)))
      print("images: " + str(len(set(img_urls))))

    soup = BeautifulSoup(source, 'html.parser')
    for link in soup.find_all('a'):
      if link.get('href') not in visited_urls and link.get('href') not in banned_urls and link.get('href') not in upcoming_urls:
        if link.get('href').startswith('GUID') and link.get('href').endswith('.html'):
          upcoming_urls.append(link.get('href'))

    for img in soup.find_all('img'):
      if img.get('src') not in img_urls:
        img_urls.append(img.get('src'))

# Step 7: Save session after all html files collected
pickle_out = open("dict.pickle","wb")
pickle.dump({
  'visited_urls': visited_urls,
  'banned_urls': banned_urls,
  'upcoming_urls': upcoming_urls,
  'img_urls': img_urls,
  'visited_img_urls': visited_img_urls
}, pickle_out)
pickle_out.close()
print("****** SESSION SAVED ******")

# Step 8: Clean image URLs
for url in img_urls:
  if not isinstance(url, str):
    img_urls.remove(url)
  elif not url.startswith('GUID'):
    img_urls.remove(url)

# Step 9: Sanity check on image URLs
for url in img_urls:
  if url.endswith('jpg'):
    continue
  elif url.endswith('png'):
    continue
  elif url.endswith('gif'):
    continue
  print(url)

number_of_images = len(set(img_urls))
number_of_images_downloaded = 0

# Step 10: Download images with direct requests
headers = {
"User-Agent":
  "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
}
s = requests.session()
s.headers.update(headers)
for url in set(img_urls):
  if url not in visited_img_urls:
    if number_of_images_downloaded % 200 == 0:
      pickle_out = open("dict.pickle","wb")
      pickle.dump({
        'visited_urls': visited_urls,
        'banned_urls': banned_urls,
        'upcoming_urls': upcoming_urls,
        'img_urls': img_urls,
        'visited_img_urls': visited_img_urls
      }, pickle_out)
      pickle_out.close()
      print("****** SESSION SAVED ******")

    for cookie in driver.get_cookies():
        c = {cookie['name']: cookie['value']}
        s.cookies.update(c)

    r = s.get(base_url + url, allow_redirects=True)
    open("docs/" + url, 'wb').write(r.content)
    visited_img_urls.append(url)

    print("images: " + str(number_of_images))
    print("downloaded: " + str(number_of_images_downloaded))
    number_of_images_downloaded += 1

time.sleep(25)
driver.quit()