import os
from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import concurrent.futures
import threading
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return 'JOB scraper!'

def setup_selenium_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def extract_job_details(job_element):
    try:
        # Job Title
        title_element = job_element.find_element(By.CSS_SELECTOR, 'a[class*="font-bold"]')
        title = title_element.text
        job_url = title_element.get_attribute('href')

        # Company Name
        company_element = job_element.find_elements(By.CSS_SELECTOR, 'span')
        company = company_element[0].text if company_element else 'N/A'

        # Additional Details
        details_element = job_element.find_elements(By.CSS_SELECTOR, 'span[class*="text-gray-700"]')
        details = details_element[0].text if details_element else 'N/A'


        # Logo
        logo_element = job_element.find_element(By.CSS_SELECTOR, 'img')
        logo_url = logo_element.get_attribute('src')

        return {
            'title': title,
            'company': company,
            'details': details,
            'job_url': job_url,
            'logo_url': logo_url
        }
    except Exception as e:
        print(f"Error extracting job details: {e}")
        return None

def parse_job_details(details_text):
    """
    Parse job details string to extract location, salary, and posted date
    """
    parts = [part.strip() for part in details_text.split('•')]
    result = {
        'location': 'N/A',
        'salary_range': 'N/A',
        'posted_date': 'N/A'
    }
    
    for part in parts:
        if any(country in part for country in ['United States', 'Canada', 'UK', 'Remote']):
            result['location'] = part
        elif '$' in part and 'k' in part:
            result['salary_range'] = part
        elif 'day' in part.lower():
            result['posted_date'] = part
    
    return result

@app.route('/scrape_jobs')
def scrape_jobs():
    driver = None
    try:
        """Returns jobs present on the home page"""
        driver = setup_selenium_driver()
        driver.get('https://wellfound.com/jobs')
        
        # Wait for job elements to load
        time.sleep(10)
        
        # Find all job elements
        job_elements = driver.find_elements(By.CSS_SELECTOR, 'div[class*="mb-2 flex flex-col justify-between border-b border-gray-400 py-3 transition-all duration-100 ease-linear md:flex-row"]')
        
        # Extract job details
        jobs = []
        for job_element in job_elements: 
            job_details = extract_job_details(job_element)
            if job_details:
                jobs.append(job_details)
        
        return jsonify({
            'jobs' : jobs,
            'total_jobs' : len(jobs)
                })
    
    except Exception as e:
        print(f"Scraping error: {e}")
        return jsonify({'error': str(e)}), 500
    
    finally:
        if driver:
            driver.quit()

@app.route('/soup')
def get_full_soup():
    driver = None
    try : 
        driver = setup_selenium_driver()
        driver.get('https://wellfound.com/jobs')

        time.sleep(8)
        page_source = driver.page_source
        soup = BeautifulSoup(page_source,'html.parser')
        return soup.prettify()
        
    except Exception as e:
        print(f"Soup error : {e}")
        return jsonify({"error" : str(e)})

    finally : 
        if driver : 
            driver.quit()
            
def scrape_wellfound_jobs(keywords):
    """
    Scrape jobs from Wellfound with keyword filtering
    """
    all_jobs = []
    driver = None
    try:
        driver = setup_selenium_driver()
        
        for keyword in keywords:
            # Navigate to Wellfound jobs page with keyword
            driver.get(f'https://wellfound.com/jobs?query={keyword}')
            
            # Wait for job elements to load
            WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[class*="mb-2 flex flex-col justify-between border-b border-gray-400 py-3 transition-all duration-100 ease-linear md:flex-row"]'))
            )
            
            # Find all job elements
            job_elements = driver.find_elements(By.CSS_SELECTOR, 'div[class*="mb-2 flex flex-col justify-between border-b border-gray-400 py-3 transition-all duration-100 ease-linear md:flex-row"]')
            
            # Extract job details
            for job_element in job_elements:
                try:
                    # Job Title and URL
                    title_element = job_element.find_element(By.CSS_SELECTOR, 'a[class*="font-bold"]')
                    title = title_element.text
                    job_url = title_element.get_attribute('href')

                    # Company Name
                    company_elements = job_element.find_elements(By.CSS_SELECTOR, 'span')
                    company = company_elements[0].text if company_elements else 'N/A'

                    # Additional Details
                    details_element = job_element.find_elements(By.CSS_SELECTOR, 'span[class*="text-gray-700"]')
                    details_text = details_element[0].text if details_element else 'N/A'
                    additional_details = parse_job_details(details_text)

                    # Logo
                    logo_element = job_element.find_element(By.CSS_SELECTOR, 'img')
                    logo_url = logo_element.get_attribute('src')

                    # Create job entry
                    job_entry = {
                        'keyword': keyword,
                        'title': title,
                        'company': company,
                        'location': additional_details['location'],
                        'salary_range': additional_details['salary_range'],
                        'posted_date': additional_details['posted_date'],
                        'job_url': job_url,
                        'logo_url': logo_url
                    }
                    all_jobs.append(job_entry)
                
                except Exception as e:
                    print(f"Error extracting individual job: {e}")
            
            time.sleep(2)  # Brief pause between keyword searches
        
        return all_jobs
    
    except Exception as e:
        print(f"Scraping error: {e}")
        return []
    
    finally:
        if driver:
            driver.quit()

@app.route('/search_jobs', methods=['POST'])
def search_jobs():
    keywords = request.json.get('keywords', [])
    
    if not keywords:
        return jsonify({
            'error': 'Please provide keywords',
            'status': 'failed'
        }), 400
    
    # Scrape jobs
    jobs = scrape_wellfound_jobs(keywords)
    
    # Aggregate companies by keyword
    companies_by_keyword = {}
    for job in jobs:
        keyword = job['keyword']
        if keyword not in companies_by_keyword:
            companies_by_keyword[keyword] = set()
        companies_by_keyword[keyword].add(job['company'])
    
    return jsonify({
        'total_jobs_found': len(jobs),
        'jobs': jobs,
        'companies_by_keyword': {k: list(v) for k, v in companies_by_keyword.items()}
    })