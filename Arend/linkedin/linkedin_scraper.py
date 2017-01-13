from bs4 import BeautifulSoup
from selenium import webdriver
import csv
import json
import time
import re

driver = webdriver.Firefox()
login = "https://www.linkedin.com/uas/login"

pages= ["https://www.linkedin.com/company-beta/8545501/",
        "https://www.linkedin.com/company-beta/1062181/",
        "https://www.linkedin.com/company-beta/3850436",
        "https://www.linkedin.com/company-beta/9357034/",
        "https://www.linkedin.com/company-beta/62059/",
        "https://www.linkedin.com/company-beta/32757/"
        ]

count = 0

# Login as User
driver.get(login)
email = driver.find_element_by_id("session_key-login")
password = driver.find_element_by_id("session_password-login")
email.send_keys("pascal.kunkler@gmail.com")
password.send_keys("Pascalk_170395")
driver.find_element_by_name("signin").click()
time.sleep(5)

with open('linkedin_analysis.csv', 'w') as file:
    w = csv.writer(file)
    w.writerow(['company', 'employees', 'employees_on_linkedin', 'follower',
                'updates', 'open_jobs'])

    #Scrape pages
    for profile in pages:
        driver.get(profile)
        time.sleep(5)

        #Scroll to bottom and try as long as change appears
        lastHeight = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            newHeight = driver.execute_script("return document.body.scrollHeight")
            if newHeight == lastHeight:
                break
            lastHeight = newHeight

        html=driver.page_source
        soup=BeautifulSoup(html, "lxml")

        name = soup.find('h1', {'class':'org-top-card-module__name mb1 Sans-26px-black-85%-light'}).getText().replace('\n', '')
        size = soup.find('span', {'class':'company-size'}).getText().replace(' ', '').replace(',', '')
        size_d = re.sub(r'[a-z]', "", size).replace('\n', '')
        employees = soup.find_all('a', {'class':'snackbar-description-see-all-link'})
        employees_count = re.sub("\D", "", employees[0].getText())
        updates = len(soup.find_all('article'))
        follower = soup.find_all('p', {'class':'org-top-card-module__followers-count Sans-15px-black-55%'})
        follower_count = re.sub("\D", "", follower[0].getText())

        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(2)
        print "Now trying to go to Jobs page..."
        link = driver.find_element_by_link_text('See jobs')
        link.click()
        time.sleep(5)

        html1 = driver.page_source
        soup1 = BeautifulSoup(html1, "lxml")
        jobs = soup1.find('div', {'class':'results-context'})
        jobs_count = re.sub("\D", "", jobs.getText())

        print "-"*20
        print "Company: ", name
        print "Size: ", size_d
        print "Follower: ", follower_count
        print "Employees on LinkedIn: ", employees_count
        print "Updates: ", updates
        print "Current Jobs: ", jobs_count
        print "-"*20

        w.writerow([name, size_d, employees_count, follower_count,
                    updates, jobs_count])
        count += 1

print "\nSuccess! {} companies scraped.".format(count)
driver.close()
