import { useState } from "react";
import { Badge } from "./ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "./ui/select";

// Define the type for the companies data
type CompaniesData = {
  [key: string]: string[];
};

interface CompaniesDataProps {
    companiesData : CompaniesData
}

export function CompaniesByKeyword({companiesData} : CompaniesDataProps) {
  const [selectedCategory, setSelectedCategory] = useState<string>("");
  const categories = Object.keys(companiesData);

  const handleCategoryChange = (category: string) => {
    setSelectedCategory(category);
  };

  return (
    <Card className="w-full max-w-4xl mx-auto">
      <CardHeader>
        <CardTitle>Companies by Keyword</CardTitle>
        <div className="mt-2">
          <Select onValueChange={handleCategoryChange}>
            <SelectTrigger className="w-[180px]">
              <SelectValue placeholder="Select Category" />
            </SelectTrigger>
            <SelectContent>
              {categories.map((category) => (
                <SelectItem key={category} value={category}>
                  {category.charAt(0).toUpperCase() + category.slice(1)}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>
      </CardHeader>
      <CardContent>
        {selectedCategory && (
          <div className="flex flex-wrap gap-2">
            {companiesData[selectedCategory].map((company:any) => (
              <Badge key={company} variant="secondary" className="text-sm">
                {company}
              </Badge>
            ))}
          </div>
        )}
        {!selectedCategory && (
          <p className="text-muted-foreground">
            Select a category to view companies
          </p>
        )}
      </CardContent>
    </Card>
  );
}
