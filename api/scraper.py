import os
import time
import json
from typing import List, Dict

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

from models import JobListingSearchResult
from utils import parse_job_listing

class WellfoundScraper:
    def __init__(self, email: str, password: str):
        """
        Initialize Wellfound Scraper with Chrome WebDriver
        
        Args:
            email (str): Wellfound login email
            password (str): Wellfound login password
        """
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in background
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), 
            options=chrome_options
        )
        
        self.email = email
        self.password = password

    def login(self) -> bool:
        """
        Login to Wellfound
        
        Returns:
            bool: Login successful status
        """
        try:
            self.driver.get("https://wellfound.com/login")
            time.sleep(3)

            email_input = self.driver.find_element("id", "user_email")
            email_input.send_keys(self.email)

            password_input = self.driver.find_element("id", "user_password")
            password_input.send_keys(self.password)

            login_button = self.driver.find_element("name", "commit")
            login_button.click()

            time.sleep(5)
            return "/jobs" in self.driver.current_url
        except Exception as e:
            print(f"Login error: {e}")
            return False

    def scrape_jobs(
        self, 
        keywords: List[str] = [], 
        max_pages: int = 10
    ) -> List[Dict]:
        """
        Scrape job listings from Wellfound
        
        Args:
            keywords (List[str]): Keywords to filter jobs
            max_pages (int): Maximum number of pages to scrape
        
        Returns:
            List[Dict]: Scraped job listings
        """
        if not self.login():
            raise Exception("Login failed")

        all_job_listings = []

        for page in range(1, max_pages + 1):
            js_script = f"""
            var callback = arguments[0];
            var xhr = new XMLHttpRequest();
            xhr.open('POST', 'https://wellfound.com/graphql?fallbackAOR=talent', true);
            xhr.setRequestHeader('Content-Type', 'application/json');
            xhr.onreadystatechange = function() {{
                if (xhr.readyState == 4) {{
                    if (xhr.status == 200) {{
                        callback(xhr.responseText);
                    }} else {{
                        callback("Error: " + xhr.statusText);
                    }}
                }}
            }};
            xhr.send(JSON.stringify({{
                "operationName": "JobSearchResultsX",
                "variables": {{
                    "filterConfigurationInput": {{
                        "page": {page},
                        "keywords": {json.dumps(keywords)},
                        "jobTypes": ["full_time"],
                        "remotePreference": "REMOTE_OPEN"
                    }}
                }},
                "extensions": {{
                    "operationId": "tfe/b898ee628dd3385e1b8c467e464a0261ad66c478eda6e21e10566b0ca4ccf1e9"
                }}
            }}));
            """

            response = self.driver.execute_async_script(js_script)
            response_data = json.loads(response)

            job_listings = response_data['data']['talent']['jobSearchResults']['startups']['edges']
            
            for startup in job_listings:
                startup_name = startup['node']['name']
                for job in startup['node']['highlightedJobListings']:
                    job_result = JobListingSearchResult(
                        typename=job['__typename'],
                        atsSource=job.get('atsSource'),
                        autoPosted=job.get('autoPosted', False),
                        currentUserApplied=job.get('currentUserApplied', False),
                        description=job.get('description', ''),
                        id=job.get('id', ''),
                        jobType=job.get('jobType', ''),
                        lastRespondedAt=job.get('lastRespondedAt'),
                        liveStartAt=job.get('liveStartAt', ''),
                        primaryRoleTitle=job.get('primaryRoleTitle', ''),
                        remote=job.get('remote', False),
                        reposted=job.get('reposted', False),
                        slug=job.get('slug', ''),
                        title=job.get('title', ''),
                        compensation=job.get('compensation'),
                        usesEstimatedSalary=job.get('usesEstimatedSalary', False)
                    )
                    
                    # Add startup name to job listing
                    parsed_job = parse_job_listing(job_result)
                    parsed_job['startup_name'] = startup_name
                    
                    all_job_listings.append(parsed_job)

            # Check if there are more pages
            has_next_page = response_data['data']['talent']['jobSearchResults'].get('hasNextPage', False)
            if not has_next_page:
                break

        return all_job_listings

    def __del__(self):
        """Close WebDriver when object is deleted"""
        if hasattr(self, 'driver'):
            self.driver.quit()