import datetime, time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


from django.contrib.auth.models import User
from blog.models import Post
from blog.models import Comment, Product, ProductData


from apscheduler.schedulers.background import BackgroundScheduler

def job():
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option(
        "prefs", {"prfile.managed_default_content_setting.images": 2})

    driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=options)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                        "source": """ Object.defineProperty(navigator, 'webdriver', { get: () => undefined }) """})

    products=Product.objects.all()
    for product in products:
        driver.get(product.url)
        driver.implicitly_wait(10) 
        time.sleep(3)
        element=driver.find_element(By.XPATH, """//*[@id="contents"]/div[1]/div/div[3]/div[5]/div[1]/div/div[3]/span[1]/strong""").text
        if not element:
            element=driver.find_element(By.XPATH, """//*[@id="contents"]/div[1]/div/div[3]/div[5]/div[1]/div/div[2]/span[1]/strong""").text
        price=int(element[:-1].replace(',', ''))
        data, already=ProductData.objects.get_or_create(product=product, price=price, time=datetime.datetime.now())
        if not already:
            if data.price>price:
                ProductData.objects.update(product=product, price=price)        

        
    driver.quit()
    return

def main():
    sched = BackgroundScheduler()
    sched.add_job(job,'interval', seconds=10, id='test')
    sched.start()