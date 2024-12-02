import { Job } from "@/lib/types";
import { JobCard } from "@/components/jobcard"

interface JobGridProps {
  jobs: Job[];
}

export function JobGrid({ jobs }: JobGridProps) {
  return (
    <div className="mt-2 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {jobs.map((job) => (
        <JobCard key={`${job.company}-${job.title}`} job={job} />
      ))}
    </div>
  );
}