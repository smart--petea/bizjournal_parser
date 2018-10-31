import pymongo

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

mongoclient = pymongo.MongoClient("mongodb://localhost:27017/")
bizdb = mongoclient['bizjournal']
bizcol = bizdb['bizjournal']

driver = webdriver.Chrome()

while 1:
    cursor = bizcol.find({"url": None}).limit(1);
    if cursor.count() == 0:
        break

    document = cursor[0]
    print document['href']

    driver.get(document['href'])

    WebDriverWait(driver, 1000).until(
            EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "child-definition")]'))
    )

    el = driver.find_element_by_xpath('//div[contains(@class, "child-definition")]//a')
    url = el.get_attribute('href')
    print "get - %s" % url
    document['url'] = url
    bizcol.update({"_id": document["_id"]}, document, True)


driver.close()
print "no more empty hrefs"
