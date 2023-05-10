from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import pandas as pd
from alive_progress import alive_bar
import sys

#starts up chrome
driver = webdriver.Chrome(service = Service('./chromedriver'))

#collect our data here
file = open('indeed.csv','a')
file.write(f'title,company,rating,location,salary,part_time,link\n')

start = 0

with alive_bar(58,bar='bubbles',spinner=None,dual_line=True) as bar:
    while start < 580:
        bar()
        #visit webpage
        driver.get(f'https://indeed.com/jobs?q=data+scientist&l=new+york+city&start={start}')

        #get the list of jobs on that page
        jobs = driver.find_elements(By.CLASS_NAME,'job_seen_beacon')

        #add the job details to our data
        for job in jobs:

            title = job.find_element(By.TAG_NAME,'a').text

            if title == '':
                continue

            link = job.find_element(By.TAG_NAME,'a').get_attribute('href')

            company = job.find_element(By.CLASS_NAME,'companyName').text

            try:
                rating = job.find_element(By.CLASS_NAME,'ratingNumber').text
            except:
                rating = 'na'

            location = job.find_element(By.CLASS_NAME,'companyLocation').text.split('\n')[0]

            try:
                tags = job.find_element(By.CSS_SELECTOR,'.heading6.tapItem-gutter.metadataContainer.noJEMChips.salaryOnly').text.split('\n')
                salary = tags[0]

                if len(tags)>1 and tags[1] == 'Part-time':
                    part_time = 'true'
                else:
                    part_time = 'false'
                
            except:
                salary = 'na'
                part_time = 'false'

            file.write(f'{title},{company},{rating},{location},{salary},{part_time},{link}\n')

        start += 10

driver.close()
