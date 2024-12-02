import { Job } from "@/lib/types";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

interface JobCardProps {
  job: Job;
}

export function JobCard({ job }: JobCardProps) {
  return (
    <a href={job.job_url} target="_blank" rel="noopener noreferrer">
      <Card className="h-full hover:shadow-lg transition-shadow duration-200">
        <CardHeader className="flex flex-row items-center gap-4">
          <div className="flex flex-col">
            <h3 className="font-semibold text-lg">{job.title}</h3>
            <p className="text-sm text-muted-foreground">{job.company}</p>
          </div>
        </CardHeader>
        <CardContent>
          <div className="flex flex-col gap-2">
            <div className="flex items-center gap-2">
              {job.location !== "N/A" && (
                <Badge variant="secondary">{job.location}</Badge>
              )}
              {job.salary_range !== "N/A" && (
                <Badge variant="outline">{job.salary_range}</Badge>
              )}
            </div>
            <p className="text-sm text-muted-foreground mt-2">
              Posted {job.posted_date}
            </p>
          </div>
        </CardContent>
      </Card>
    </a>
  );
}