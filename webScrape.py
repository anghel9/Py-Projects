import time
from bs4 import BeautifulSoup
import requests

unfamiliar_skill = []
i = 0 
while True:
    user_input = input('Type unfamiliar skill, type q to quit: ')
    if user_input.lower() == 'q':
        break
    unfamiliar_skill.append(user_input)

print(f"Filtering out {unfamiliar_skill}")
print('')

def find_jobs():
    html_text=requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&searchTextSrc=&searchTextText=&txtKeywords=Python&txtLocation=').text
    soup = BeautifulSoup(html_text, 'lxml')
    jobs = soup.find_all('li', class_ = 'clearfix job-bx wht-shd-bx')
    for job in jobs:
        published_date= job.find('span', class_ = 'sim-posted').span.text
        if 'few' in published_date:
            comp_name = job.find('h3', class_ = 'joblist-comp-name').text.replace(' ','')
            skills = job.find('span', class_ ='srp-skills').text.replace(' ','')
            more_info= job.header.h2.a['href']
            if unfamiliar_skill[i] not in skills:
                print(f"Company Name:{comp_name.strip()}")
                print(f"Required Skills: {skills.strip()}")
                print(f'More Info: {more_info}')
                print('')
                ++i

if __name__ == '__main__':
    while True:
        find_jobs()
        time_wait=10
        print(f'Waiting {time_wait} min....')
        time.sleep(time_wait * 60)