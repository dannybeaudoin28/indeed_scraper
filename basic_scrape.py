from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

import os

from open_api import get_gpt_response
from python_docx import create_resume, get_old_resume_info

def init():
    old_resume_info = get_old_resume_info()
    old_resume = old_resume_info[0]
    old_header = old_resume_info[1]

    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920,1200")
    chrome_options.add_argument('--disable-gpu')  # Disable GPU acceleration (required if running on Windows)
    chrome_options.add_argument('--no-sandbox')  # Bypass OS security model (necessary for some environments)
    chrome_options.add_argument('--disable-dev-shm-usage')  # Overcome limited resource problems
    chrome_options.add_argument(f'user-agent={user_agent}')
    
    jobs = get_jobs(chrome_options)
    # print_card_details(jobs)
    for job in jobs:
        job_details = get_job_details(job, chrome_options)
        gpt_res = get_gpt_response(job_details[0], old_resume)
        dir_name = job_details[1] # [:12] substring TODO: Must modify title to strip it of unusable characters
        create_dir(dir_name)
        create_resume(gpt_res, job_details[1], old_header, dir_name)
        create_url_file(dir_name, job["link"])
        

def get_jobs(options):
    search_job_title = input("What position would you like to search for? ")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # url = 'https://ca.indeed.com/jobs?q=programmer&l=Remote&jt=subcontract&ts=1719700838600&pts=1719322684741&rbsalmin=0&rbsalmax=0&sc=0kf%3Ajt%28subcontract%29%3B&rq=1&from=HPRecent&rsIdx=0&vjk=21ee3928298d4ebf'
    # url = 'https://ca.indeed.com/jobs?q=Programmer&l=Kingston%2C+ON'
    url = 'https://ca.indeed.com/jobs?q=' + search_job_title + '&l=Kingston'
    
    print(f"You are using the following URL: {url}")

    driver.get(url)

    wait = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, 'slider_item')))

    # Scroll to load more jobs (if needed)
    for _ in range(5):  # Adjust the range for more scrolling
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    driver.quit()

    job_cards = soup.find_all('div', class_='slider_item')
    
    jobs = set_card_data(job_cards=job_cards)
    
    return jobs
    
    
def set_card_data(job_cards):
    jobs = []
    for card in job_cards:
        title = card.find('h2', class_='jobTitle').get_text(strip=True)
        company = card.find('span', class_='css-63koeb').get_text(strip=True)
        location = card.find('div', class_='css-1p0sjhy').get_text(strip=True)
        job_link = 'https://ca.indeed.com' + card.find('a', class_='jcs-JobTitle')['href']
        jobs.append({
            'title': title,
            'company': company,
            'location': location,
            'link': job_link
    })
    return jobs


def print_card_details(jobs):
    for job in jobs:
        print(f"Title: {job['title']}")
        print(f"Company: {job['company']}")
        print(f"Location: {job['location']}")
        print(f"Link: {job['link']}")
        print('-' * 40)
        
        
def get_job_details(job, options):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    #This line should be grabbing the results of each individual link from the indeed homesearch page
    job_link = job['link']  
    job_title = job['title']
        
    driver.get(job_link)

    wait = WebDriverWait(driver, 1)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'fastviewjob')))

    for _ in range(5):  
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)  

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    driver.quit()

    job_data = soup.find_all('div', class_='fastviewjob')
    
    desc = ""
    
    # Retrieve each p element (data) in job_data
    for job in job_data:
        desc = job.find('div', class_='jobsearch-JobComponent-description').get_text(strip=True)
    
    return (desc, job_title)

def create_dir(dir_name):
    parent_dir = "C:/Users/jacki/Desktop/Apps/ResumeBuilder/assets/"
    path = os.path.join(parent_dir, dir_name)
    os.mkdir(path)
    
def create_url_file(dir_name, url):
    # base_path = "assets"
    full_path = "assets/" + dir_name + "/url.txt"
    f = open(full_path, "x")
    f.write(url)
    f.close()
    
             
init()