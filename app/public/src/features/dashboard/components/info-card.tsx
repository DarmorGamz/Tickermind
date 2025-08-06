import {
  HoverCard,
  HoverCardContent,
  HoverCardTrigger,
} from "@/components/ui/hover-card"
import { Info } from "lucide-react";

interface InfoCardProps {
    text?: string
    title?: string
    size?: number
}

export default function InfoCard({text, title, size}: InfoCardProps) {
  return (
    <>
    <HoverCard>
        <HoverCardTrigger>
            <Info 
                className={`w-${size} h-${size} text-muted-foreground`}
            />
        </HoverCardTrigger>
        <HoverCardContent>
            <div>
                <h4 className="text-sm font-semibold">{title}</h4>
                <div className="text-muted-foreground text-xs">
                    {text}
                </div>
            </div>
        </HoverCardContent>
    </HoverCard>
    </>
  );
}