from enum import Enum
from typing import List, Dict, Any

class Base(str, Enum):
    URL = "https://wellfound.com"
    def __str__(self):
        return str(self.value)

def parse_job_listing(job_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse job listing data into a clean dictionary format
    
    Args:
        job_data (Dict): Raw job listing data
    
    Returns:
        Dict: Cleaned job listing data
    """
    return {
        "title": job_data.title,
        "company": job_data.get('startup_name', 'Unknown'),
        "compensation": job_data.compensation,
        "job_type": job_data.jobType,
        "remote": job_data.remote,
        "description": job_data.description,
        "job_id": job_data.id,
        "slug": job_data.slug
    }