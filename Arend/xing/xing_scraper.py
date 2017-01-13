from bs4 import BeautifulSoup
from selenium import webdriver
import csv
import json
import time
import re

driver = webdriver.Firefox()

pages= ["https://www.xing.com/companies/blumenbeckergruppe",
        "https://www.xing.com/companies/arendprozessautomationgmbh",
        "https://www.xing.com/companies/ksvkoblenzersteuerungs-undverteilungsbaugmbh",
        "https://www.xing.com/companies/beckhoffautomationgmbh&co.kg",
        "https://www.xing.com/companies/pilzgmbh&co.kg"
        ]
with open('xing_analysis.csv', 'w') as file:
    w = csv.writer(file)
    w.writerow(['company', 'employees', 'employees_on_xing', 'rating', 'awards',
                'updates', 'open_jobs'])

    for profile in pages:
        driver.get(profile)
        html1=driver.page_source
        soup1=BeautifulSoup(html1, "lxml")

        #About Page (MAIN PAGE)
        name = soup1.find('div', {"class":"header-name"}).getText().replace('\n', '')
        facts=soup1.find('section', {"class": "facts"})
        employees = facts.find('dd').getText()
        try:
            rating = soup1.find('div', {"class":"kununu-rating-nr"}).getText().replace('\n', '').replace(' ', '')
            awards = soup1.find_all('a', {"class":"kununu-badge"})
        except:
            rating = None
            awards = []

        #Updates Page
        try:
            link = driver.find_element_by_link_text('Updates')
            link.click()
        except:
            posts = []

        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                button = driver.find_element_by_link_text('More')
                if button:
                    if button.is_displayed():
                        button.click()
                else:
                    break
            except:
                break

        html2=driver.page_source
        soup2=BeautifulSoup(html2, "lxml")

        #Get updates
        updates = []
        for ul in soup2.find_all('ul', {'id': 'news-feed'}):
            for li in ul.find_all('li', {'class':'activity-item'}):
                updates.append(li)

        #Get employees
        for li in soup2.find_all('li', {'id':'employees-tab'}):
            for a in li.find_all('a'):
                contacts = re.sub("\D", "", a.getText())

        #Get jobs
        for li in soup2.find_all('li', {'id':'jobs-tab'}):
            for a in li.find_all('a'):
                jobs = re.sub("\D", "", a.getText())

        print json.dumps({"name": name, "data": {
                                "employees": employees,
                                "rating": rating,
                                "updates": len(updates),
                                "contacts": contacts,
                                "awards": len(awards),
                                "jobs": jobs
                                }})

        w.writerow([name, employees, contacts, rating, len(awards), len(updates), jobs])

driver.close()
