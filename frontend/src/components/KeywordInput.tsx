import { useState } from "react";
import { Input } from "./ui/input";
import { X } from "lucide-react";
import { Button } from "./ui/button";
import { Badge } from "./ui/badge";

interface KeywordsInputProps {
    keywords: string[]
    onKeyWordsChange: (keywords: string[]) => void;
}

export function KeywordInput({keywords, onKeyWordsChange}: KeywordsInputProps) {
    const [currentKeyWord, setCurrentKeyword] = useState("")

    const handleAddKeyword = () => {
        if (currentKeyWord.trim()) {
            onKeyWordsChange([...keywords, currentKeyWord.trim()])
            setCurrentKeyword("")
        }
    }

    const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
        if (e.key === "Enter") {
            e.preventDefault();
            handleAddKeyword();
        }
    };

    const removeKeyword = (keywordToRemove: string) => {
        onKeyWordsChange(keywords.filter((k) => k !== keywordToRemove))
    }

    return (
        <div className="space-y-4">
            <div className="flex space-x-2">
                <Input 
                    value={currentKeyWord}
                    onChange={(e) => setCurrentKeyword(e.target.value)}
                    onKeyDown={handleKeyPress}
                    placeholder="Enter keywords"
                    className="px-2 py-1"
                />
                <Button
                    onClick={handleAddKeyword}
                    type="button"
                >
                    Add
                </Button>
            </div>

            <div className="flex flex-wrap gap-2">
                {keywords.map((keyword) => (
                    <Badge key={keyword} variant="secondary" className="text-sm">
                        {keyword}
                        <button onClick={() => removeKeyword(keyword)} className="ml-2">
                            <X className="h-4 w-4" />
                        </button>
                    </Badge>
                ))}
            </div>
        </div>
    )
}