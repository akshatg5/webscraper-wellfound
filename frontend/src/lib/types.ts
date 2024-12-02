export interface Job {
    company: string;
    job_url: string;
    keyword: string;
    location: string;
    logo_url: string;
    posted_date: string;
    salary_range: string;
    title: string;
  }
  
  export interface ApiResponse {
    companies_by_keyword: Record<string, string[]>;
    jobs: Job[];
  }