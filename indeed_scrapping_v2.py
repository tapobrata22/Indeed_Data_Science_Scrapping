# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 09:52:56 2019

@author: Tapobrata
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 13:36:44 2019

@author: Tapobrata
"""

"""
Created on Wed Oct  2 14:52:07 2019

@author: Tapobrata
"""

#Livemint SCRAPPING

#Importing all the necessary libraries and mentioning the path for reading the 9 CSV files
import matplotlib
import numpy as np
import random 
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import re
import time
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import xgboost
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
import math
import time
#Oxford 
from bs4 import BeautifulSoup
import urllib.request
import csv
#import httplib
import requests
import winsound
import json
from slimit import ast
from slimit.parser import Parser
from slimit.visitors import nodevisitor
from pandas import ExcelWriter
from itertools import combinations

# specify the url

main_path = 'D:/web scrapping/personal_projects'
import os
os.chdir(main_path)

city_list = ['Philadelphia','San+Francisco', 'New+York', 'California', 'Houston', 'Boston', 'Chicago', 'Seattle', 'Austin', 'Maryland']

all_company_final_summary = pd.DataFrame()

for city_index in range(0,len(city_list)):
    
    city_name = city_list[city_index]
    
    for page_index in range(1,9):
        #page_index = 1
        number = page_index * 10
        
        original_html = 'https://www.indeed.com/jobs?q=data+scientist+$65,000&l='+city_name+'&start='+str(number)
        
        #original_html = 'https://www.indeed.com/jobs?q=data+scientist+$65,000&l=California&start='+str(number)
        urlpage =  str(original_html)
        #main_word = top_10pages[i]
        # query the website and return the html to the variable 'page'
        page = urllib.request.urlopen(urlpage)
        # parse the html using beautiful soup and store in variable 'soup'
        soup = BeautifulSoup(page, 'html.parser')
        
        #Extracting all links
        
            
        #Finding meaning of words
        title = soup.findAll(attrs={"class":"headline"})
        word_meaning = str(title)
        
        #Loop to extract job roles present on page
        all_links = []
        all_roles = []
        role_list = soup.findAll('div', attrs={'class':'title'})
        for i in range(0,len(role_list)):
            #i = 0
            s = str(role_list[i])
            start = 'href='
            end = ' id='
            link = s[s.find(start)+len(start):s.rfind(end)]
            link = link.replace('"', "")
            all_links.append(link)
            title_name = str(role_list[i].text)
            title_name = title_name.strip()
            all_roles.append(title_name)
        
        
        all_podcast_links = all_links
        
        ##corect link - https://www.indeed.com/viewjob?cmp=RMDS-Lab&t=Data+Scientist&jk=614f9fbd6a80e036
        all_podcast_links = [i.split('-')[-1] for i in all_podcast_links]
        #all_podcast_links = [i.split('?fccid')[0] for i in all_podcast_links]
        
        #check_1 = [i for i in all_podcast_links if '/rc/clk' not in i]
        #begin_text = '/rc/clk?jk='
        #check_1 = [begin_text+s for s in check_1]
        #text_replace = "?fccid="
        #check_1 = [w.replace(text_replace,"&amp;fccid=") for w in check_1]
        
        modified_links = []
        for i in range(0,len(all_podcast_links)):
            main_link_text = all_podcast_links[i]
            string_find = '/rc/clk'
            if(main_link_text.find(string_find) == -1):
                main_link_text = '/rc/clk?jk=' + main_link_text
                text_replace = "?fccid="
                main_link_text = main_link_text.replace(text_replace, '&amp;fccid=')
                print('Link modified for link number', i)
            else:
                main_link_text = main_link_text
            modified_links.append(main_link_text)
        
        text_delete = '/rc/clk'
        #text_replace = "/company/"
        all_podcast_links = [w.replace(text_delete,"") for w in modified_links]
        #all_podcast_links = [w.replace(text_replace,"cmp=") for w in all_podcast_links]
        text_replace = "/jobs/"
        all_podcast_links = [w.replace(text_replace,"&t=") for w in all_podcast_links]
        text_to_add = 'https://www.indeed.com/viewjob?'
        final_links = [text_to_add+s for s in all_podcast_links]
        text_replace = "/viewjob?/company/"
        final_links = [w.replace(text_replace,"/company/") for w in final_links]
        
        
        all_companies = []
        company_list = soup.findAll('span', attrs={'class':'company'})
        for i in range(0,len(company_list)):
            #i = 2
            comp_name = str(company_list[i].text)
            comp_name = comp_name.strip()
            all_companies.append(comp_name)
            
        all_locations = []
        location_list = soup.findAll('span', attrs={'class':'location accessible-contrast-color-location'})
        for i in range(0,len(location_list)):
            #i = 2
            loc_name = str(location_list[i].text)
            loc_name = loc_name.strip()
            all_locations.append(loc_name)
        
        all_job_summary = []
        job_summary_list = soup.findAll('div', attrs={'class':'summary'})
        for i in range(0,len(location_list)):
            #i = 2
            job_summary = str(job_summary_list[i].text)
            job_summary = job_summary.strip()
            all_job_summary.append(job_summary)
            
           
        full_company_df = pd.DataFrame(
            {'Company_Name': all_companies,
             'Role': all_roles,
             'Job_Summary': all_job_summary,
             'Location' :all_locations, 
             'JD_Link' :final_links
            })
        
        
        
        
        
        all_company_df = pd.DataFrame()
        ###Opening links present in the page###Opening links present in the page###Opening links present in the page###Opening links present in the page###Opening links present in the page
        ###Opening links present in the page###Opening links present in the page###Opening links present in the page###Opening links present in the page###Opening links present in the page
        for i in range(0, len(full_company_df)):
            #i = 0
            new_link = full_company_df['JD_Link'][i]
            urlpage =  str(new_link)
            #main_word = top_10pages[i]
            # query the website and return the html to the variable 'page'
            page = urllib.request.urlopen(urlpage)
            # parse the html using beautiful soup and store in variable 'soup'
            soup = BeautifulSoup(page, 'html.parser')
            
            script = soup.find('script')
            
            #company_name = soup.select('h4.jobsearch-CompanyReview--heading')[0].text.strip()
        
            divs = soup.find_all('div',attrs={"id" : "jobDescriptionText"})
            for d in divs:
                job_description = str(d.text)
            #Creating master_Dataframe
            
            master_df = pd.DataFrame({'JD_Link' : urlpage, 'job_description' : job_description}, index = [0])
            all_company_df = all_company_df.append(master_df)
            print('JD extracted for ', (i+1), "out of -", len(full_company_df))
        
        ####Rough below####Rough below####Rough below####Rough below####Rough below####Rough below
        ####Rough below####Rough below####Rough below####Rough below####Rough below####Rough below
        ####Rough below####Rough below####Rough below####Rough below####Rough below####Rough below
        
        full_company_df = pd.merge(full_company_df, all_company_df, on = ['JD_Link'], how = 'left')
        all_company_final_summary = all_company_final_summary.append(full_company_df)
        print('Page Number Done - ', (page_index+1), "out of -", 10, 'for city  =', city_name)



results_path = 'D:/web scrapping/indeed_job_scrapping/city_wise_results'
os.chdir(results_path)
time1 = time.strftime("%m%d-%H%M")
folder_name = "all_cities_data_science_jobs" + time1
writer = ExcelWriter(folder_name+ '_update.xlsx')
all_company_final_summary.to_excel(writer, 'all_summary_roles', index = False)
#survey_cartocar.to_excel(writer , 'merged_survey_cartocar')
writer.save()


#Finding meaning of words



#duration = 1000  # milliseconds
#freq = 440  # Hz
#winsound.Beep(freq, duration)
#time1 = time.strftime("%m%d-%H%M")
#all_words_df.to_csv(time1+'all_results_livemint' +'.csv')




