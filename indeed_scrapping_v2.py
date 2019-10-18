
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 13:36:44 2019

@author: Tapobrata
"""



#Importing all the necessary libraries
import matplotlib
import numpy as np
import random 
import os
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import re
import time
import matplotlib.pyplot as plt
import time
from bs4 import BeautifulSoup
import urllib.request
from pandas import ExcelWriter
from itertools import combinations

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
        all_podcast_links = [w.replace(text_delete,"") for w in modified_links]
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
        for i in range(0, len(full_company_df)):
            #i = 0
            new_link = full_company_df['JD_Link'][i]
            urlpage =  str(new_link)
            page = urllib.request.urlopen(urlpage)
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
       
        
        full_company_df = pd.merge(full_company_df, all_company_df, on = ['JD_Link'], how = 'left')
        all_company_final_summary = all_company_final_summary.append(full_company_df)
        print('Page Number Done - ', (page_index+1), "out of -", 10, 'for city  =', city_name)



results_path = 'D:/web scrapping/indeed_job_scrapping/city_wise_results'
os.chdir(results_path)
time1 = time.strftime("%m%d-%H%M")
folder_name = "all_cities_data_science_jobs" + time1
writer = ExcelWriter(folder_name+ '_update.xlsx')
all_company_final_summary.to_excel(writer, 'all_summary_roles', index = False)
writer.save()





#duration = 1000  # milliseconds
#freq = 440  # Hz
#winsound.Beep(freq, duration)
#time1 = time.strftime("%m%d-%H%M")
#all_words_df.to_csv(time1+'all_results_livemint' +'.csv')




