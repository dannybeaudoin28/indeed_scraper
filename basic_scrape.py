from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

def init():
    jobs = initialize()
    # print_card_details(jobs)
    for job in jobs:
        get_job_desc(job)
        #TODO   assign result of get_job_desc to list
        #       run get_chat_gpt_response(job)
        #       make new directory named job['title']
        #       save job['link'] as well as new text document containing gpt response

def initialize():
    # Configure Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Comment out this line to see the browser window
    chrome_options.add_argument('--disable-gpu')  # Required if running on Windows

    # Initialize the WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    # URL of the Indeed search page
    url = 'https://ca.indeed.com/jobs?q=programmer&l=Remote&jt=subcontract&ts=1719700838600&pts=1719322684741&rbsalmin=0&rbsalmax=0&sc=0kf%3Ajt%28subcontract%29%3B&rq=1&from=HPRecent&rsIdx=0&vjk=21ee3928298d4ebf'

    # Open the URL
    driver.get(url)

    # Wait for the page to load completely
    wait = WebDriverWait(driver, 3)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'slider_item')))

    # Scroll to load more jobs (if needed)
    for _ in range(5):  # Adjust the range for more scrolling
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Adjust sleep time as necessary

    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Close the driver
    driver.quit()

    # Find all job cards
    job_cards = soup.find_all('div', class_='slider_item')
    
    jobs = set_card_data(job_cards=job_cards)
    
    return jobs
    
    
def set_card_data(job_cards):
    # Extract job details
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
# Print job details
    for job in jobs:
        print(f"Title: {job['title']}")
        print(f"Company: {job['company']}")
        print(f"Location: {job['location']}")
        print(f"Link: {job['link']}")
        print('-' * 40)
        
        
def get_job_desc(job):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    #This line should be grabbing the results of each individual link from the indeed homesearch page
    job_link = job['link']  # Retrieve the 'link' key from the job dictionary
    # print("Link = " + job_link)
    
    driver.get(job_link)

    # Wait for the page to load completely
    wait = WebDriverWait(driver, 3)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'fastviewjob')))

    # Scroll to load more jobs (if needed)
    for _ in range(5):  # Adjust the range for more scrolling
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)  # Adjust sleep time as necessary

    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Close the driver
    driver.quit()

    # Find all job cards
    job_data = soup.find_all('div', class_='fastviewjob')
    
    data = []
    
    # Retrieve each p element (data) in job_data
    for job in job_data:
        print(job.find('div', class_='jobsearch-JobComponent-description').get_text(strip=True))
        # desc = job.find('div', class_='jobsearch-JobComponent-description').get_text(strip=True)
    #     data.append({
    #         'description': desc,
    #     })
    # return data      
 
def get_chat_gpt_response():
    #TODO   Connect to Chat Gpt API 
    #       Input job advertisement desc, and users original resume
    #       return httpResponse text of chatGPT result 
    return False      
         
init()