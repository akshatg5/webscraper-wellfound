import os
from flask import Flask, jsonify, request
import json
from flask_cors import CORS
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
from dotenv import load_dotenv
from scraper import WellfoundScraper

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return 'JOB scraper!'
    
@app.route('/scrape_jobs', methods=['POST'])
def scrape_jobs():
    """
    Endpoint to scrape job listings
    
    Expects JSON payload with optional 'keywords' and 'max_pages'
    """
    try:
        data = request.get_json() or {}
        keywords = data.get('keywords', [])
        max_pages = data.get('max_pages', 5)

        # Get credentials from environment variables
        email = os.getenv('WELLFOUND_EMAIL')
        password = os.getenv('WELLFOUND_PASSWORD')

        if not email or not password:
            return jsonify({
                "error": "Missing Wellfound credentials. Set WELLFOUND_EMAIL and WELLFOUND_PASSWORD in .env"
            }), 400

        scraper = WellfoundScraper(email, password)
        jobs = scraper.scrape_jobs(keywords, max_pages)

        return jsonify({
            "jobs": jobs,
            "total_jobs": len(jobs)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.errorhandler(Exception)
def handle_error(error):
    """Global error handler"""
    return jsonify({"error": str(error)}), 500