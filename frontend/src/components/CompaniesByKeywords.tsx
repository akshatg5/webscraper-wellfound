import { useState } from "react"
import { Card, CardHeader, CardTitle } from "./ui/card"
import { Select, SelectTrigger } from "./ui/select"

interface CompaniesData {
    [key : string] : string[]''
}

export default function CompaniesByKeyword() {
    const [selectedCategory,setSelectedCategory] = useState('')

    const handleCategoryChannge = (category : string) => {
        setSelectedCategory(category)
    }

    return (
        <Card className="w-full max-w-4xl mx-auto">
            <CardHeader>
                <CardTitle>Companies By Keyword</CardTitle>
                <div className="mt-2">
                    <Select onValueChange={handleCategoryChannge}>
                        <SelectTrigger>
                            
                        </SelectTrigger>
                    </Select>
                </div>
            </CardHeader>
        </Card>
    )
}