from selenium import webdriver
from selenium_stealth import stealth
from bs4 import BeautifulSoup
import time

import os
import requests
import pickle

from secrets import tesla_login

# Step 0: Indicate which manual you plan to scrape, currently set to Model 3
service_manual_index = "https://service.tesla.com/docs/Model3/ServiceManual/en-us/index.html"

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
driver = tesla_login(driver)

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

# Step 4: Set up Python pickle to save session.  You can stop the script and run it again to resume where you left off.
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

# Step 5: Loop to get all the html pages, and store information about images to be downloaded later.
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
      driver.get('https://service.tesla.com/docs/Model3/ServiceManual/en-us/' + url)
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

# Step 6: Save session after all html files collected
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

# Step 7: Clean image URLs
for url in img_urls:
  if not isinstance(url, str):
    img_urls.remove(url)
  elif not url.startswith('GUID'):
    img_urls.remove(url)

# Step 8: Sanity check on image URLs
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

# Step 9: Download images with direct requests
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

    r = s.get('https://service.tesla.com/docs/Model3/ServiceManual/en-us/' + url, allow_redirects=True)
    open("docs/" + url, 'wb').write(r.content)
    visited_img_urls.append(url)

    print("images: " + str(number_of_images))
    print("downloaded: " + str(number_of_images_downloaded))
    number_of_images_downloaded += 1

time.sleep(25)
driver.quit()