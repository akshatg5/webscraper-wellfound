# Wellfound Job Scraper

## Setup and Installation

1. Clone the repository:

```
    git clone https://github.com/akshatg5/webscraper-wellfound.git
```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up your `.env` file with Wellfound credentials
   - `WELLFOUND_EMAIL`: Your Wellfound login email
   - `WELLFOUND_PASSWORD`: Your Wellfound login password

5. Run the Flask application:
   ```
   flask --app api/index.py run
   ```

## API Endpoint

### Scrape Jobs
- **Endpoint**: `/scrape_jobs`
- **Method**: POST
- **Request Body**: 
  ```json
  {
    "keywords": ["python", "django"],
    "max_pages": 5
  }
  ```
- **Response**:
  ```json
  {
    "jobs": [...],
    "total_jobs": 25 (example)
  }
  ```

## Notes
- Requires Chrome WebDriver
- Uses Selenium for web scraping
- Headless browser mode for background scraping
- use the Frontend UI to select Keywords and then add that and search for jobs accordingly.