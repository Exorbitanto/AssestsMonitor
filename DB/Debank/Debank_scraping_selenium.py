from helium import *
from bs4 import BeautifulSoup
import time

url = "https://debank.com/profile/0x09d4083ffd20d21acb9118465ad7c52ac8b548f7"

browser = start_firefox(url, headless=True)
time.sleep(15)
soup = BeautifulSoup(browser.page_source, "html.parser")

assets = soup.find("div",{"class":"HeaderInfo_totalAsset__2noIk"})
print(assets)