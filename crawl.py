from bs4 import BeautifulSoup
from selenium import webdriver as wd
import requests

options = wd.ChromeOptions()
options.add_argument("headless")
options.add_argument("window-size=1920x1080")
options.add_argument("disable-gpu")
# PROXY = "127.0.0.1:8080"
# options.add_argument("--proxy-server=http://%s" % PROXY)
# options.add_argument("proxy-server=localhost:8080")
driver = wd.Chrome(executable_path="chromedriver_win32/chromedriver.exe", chrome_options=options)

url = "https://finger-warmup.chals.damctf.xyz/"
driver.get(url)
# driver.implicitly_wait(3)
# driver.get_screenshot_as_file("naver_main_headless.png")


while True:
    driver.findElement(
        By.linkText("click here, if you are patient enough I will give you the flag")
    ).click()
    body = driver.page_source
    if body.find("dam") is not -1:
        print(body)
        break
driver.quit()
print("hel")

