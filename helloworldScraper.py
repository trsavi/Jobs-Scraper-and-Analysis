# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 16:24:41 2021

@author: HP
"""

from selenium import webdriver
from bs4 import BeautifulSoup as bs
import pandas as pd
import re

driver = webdriver.Chrome('C:/Users/HP/Downloads/chromedriver.exe')

# Function that parser through page and returns bs content
def parse_page(url):
    try:
        driver.get(url)
        content = driver.page_source
        soup = bs(content,'html.parser')
        return soup
    except:
        pass

title_list = []
employer_list = []
locations_date_list = []
technology_list = []
tech_list = []
company_list = []

company_dict={'Title':[], 'Company':[], 'Location':[],'Technologies':[]}

for page in range(0,1223,30):
    if page==0:
        
        url = 'https://www.helloworld.rs/oglasi-za-posao/'
    else: 
        url = 'https://www.helloworld.rs/oglasi-za-posao?page=' + str(page) + '&show_more=1' + '&disable_saved_search=1'
    soup = parse_page(url)
    try:
        info = soup.find(class_ = 'search-results')
        jobs = info.find_all(class_ = 'col-sm-9')
        titles = info.find_all(class_='job-link')
        for title in titles:
            title = title.get_text()
            title = re.sub('\s+', '', title)
            company_dict['Title'].append(title)
            
        for job in jobs:
            employers = job.find_all(class_='-employer')
            locations = job.find_all(class_='city-time-contain')
            technologies = job.find(class_='jobtags')
            
            for tech in technologies.findAll('a'):
                tech = tech.get_text()
                tech = re.sub('\s+', '', tech)
                tech_list.append(tech)
            
            for employer in employers:
                employer = employer.get_text()
                employer = re.sub('\s+', '', employer)
                company_dict['Company'].append(employer)
                
            for location in locations:
                location = location.get_text()
                location = re.sub('\s+', '', location)
                company_dict['Location'].append(location)
                
            
                
            company_dict['Technologies'].append(tech_list)
            tech_list = []
    except:
        pass


print(company_dict)

data = pd.DataFrame.from_dict(company_dict,orient='index')
data = data.transpose()
data.to_csv('jobsHelloWorld.csv')
#print(len(title_list), len(employer_list), len(locations_date_list), len(technology_list))
    
