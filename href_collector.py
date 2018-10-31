import pymongo

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

mongoclient = pymongo.MongoClient("mongodb://localhost:27017/")
bizdb = mongoclient['bizjournal']
bizcol = bizdb['bizjournal']

cursor = bizcol.find({}).sort("_id",  -1).limit(1);
if cursor.count() == 0 :
    page = 0
else:
    page = int(cursor[0]['page'])

print page

driver = webdriver.Chrome()

while 1:
    page = page + 1
    print "Page %d \n\n" % page
    driver.get('https://www.bizjournals.com/profiles/company?q=&s=2&pl=%d' % page);


    WebDriverWait(driver, 1000).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(@class, 'primary')]//a[contains(@class,'item')]"))
    )

    els = driver.find_elements(By.XPATH, "//*[contains(@class, 'primary')]//a[contains(@class,'item')]")

    for el in els:
        print el.get_attribute('href')

        toinsert = {
                'page': page,
                'href': el.get_attribute('href')
        }
        bizcol.insert_one(toinsert)

    mongoclient.fsync()

driver.close()
