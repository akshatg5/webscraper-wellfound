import axios from "axios";
import "./App.css";
import { JobGrid } from "./components/JobGrid";
import { useState } from "react";
import { KeywordInput } from "./components/KeywordInput";
import { Card, CardDescription, CardTitle } from "./components/ui/card";
import { Button } from "./components/ui/button";
import { CompaniesByKeyword } from "./components/CompaniesByKeywords";

interface CompaniesData {
  [key: string]: string[];
}

interface Jobs {
  jobs: any[];
  companies_by_keyword: CompaniesData;
}

function App() {
  const [error, setError] = useState("");
  const [jobs, setJobs] = useState<Jobs | null>(null);

  const fetchJobsAndCompanies = async () => {
    try {
      const res = await axios.get(
        "http://127.0.0.1:5000/scrape_jobs",
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
      setJobs(res.data);
      setError("");
    } catch (error) {
      setError("Failed to fetch jobs");
      setJobs(null);
    }
  };

  return (
    <>
      <div>
        <Card className="px-5 py-5 my-4">
          <CardTitle>Job Scraper:</CardTitle>
        </Card>
        <div className="flex justify-center">
          <Button onClick={fetchJobsAndCompanies}>Search jobs</Button>
        </div>
        {jobs?.companies_by_keyword && (
          <CompaniesByKeyword companiesData={jobs.companies_by_keyword} />
        )}
        <JobGrid jobs={jobs?.jobs || []} />
        {error && <div className="text-red-500">{error}</div>}
      </div>
    </>
  );
}

export default App;
