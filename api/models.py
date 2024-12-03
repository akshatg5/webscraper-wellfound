from typing import NamedTuple, Optional

class JobListingSearchResult(NamedTuple):
    typename: str
    atsSource: Optional[str]
    autoPosted: bool
    currentUserApplied: bool
    description: str
    id: str
    jobType: str
    lastRespondedAt: Optional[str]
    liveStartAt: str
    primaryRoleTitle: str
    remote: bool
    reposted: bool
    slug: str
    title: str
    compensation: Optional[str]
    usesEstimatedSalary: bool