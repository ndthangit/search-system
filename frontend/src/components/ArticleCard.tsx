import type { Article } from "../types/article";
import {
    Box,
    Typography,
    Link,
    Paper,
    useTheme,
} from "@mui/material";
import CalendarTodayOutlinedIcon from "@mui/icons-material/CalendarTodayOutlined";
import OpenInNewIcon from "@mui/icons-material/OpenInNew";

interface ArticleCardProps {
    article: Article;
    onClick?: (article: Article) => void;
}

export default function ArticleCard({ article, onClick }: ArticleCardProps) {
    const theme = useTheme();
    const isDark = theme.palette.mode === "dark";

    function truncateSummary(summary: string, maxLength: number = 150) {
        if (!summary) return "";
        if (summary.length <= maxLength) return summary;
        return summary.substring(0, maxLength) + "...";
    }

    function formatDate(dateString: string) {
        if (!dateString) return "";
        try {
            const date = new Date(dateString);
            return date.toLocaleDateString("vi-VN", {
                day: "numeric",
                month: "numeric",
                year: "numeric",
            });
        } catch {
            return dateString;
        }
    }

    const handleClick = () => {
        if (article.url) {
            window.open(article.url, "_blank", "noopener,noreferrer");
        }
        onClick?.(article);
    };

    return (
        <Paper
            elevation={0}
            onClick={handleClick}
            sx={{
                p: 3,
                mb: 2,
                borderRadius: 3,
                border: "1px solid",
                borderColor: isDark ? "#374151" : "#e5e7eb",
                cursor: "pointer",
                transition: "all 0.2s ease-in-out",
                "&:hover": {
                    backgroundColor: isDark ? "#334155" : "#f0f4ff",
                    borderColor: isDark ? "#4b5563" : "#3b82f6",
                    transform: "translateY(-2px)",
                    boxShadow: isDark 
                        ? "0 4px 12px rgba(0, 0, 0, 0.3)" 
                        : "0 4px 12px rgba(59, 130, 246, 0.15)",
                },
            }}
        >
            {/* Title */}
            <Typography
                variant="h6"
                component="h3"
                sx={{
                    fontWeight: 700,
                    color: "text.primary",
                    mb: 1,
                    lineHeight: 1.4,
                    fontSize: "1.1rem",
                }}
            >
                {article.title}
            </Typography>

            {/* Summary */}
            <Typography
                variant="body2"
                sx={{
                    mb: 2,
                    lineHeight: 1.7,
                    color: "text.secondary",
                }}
            >
                {truncateSummary(article.summary)}
            </Typography>

            {/* Footer: Date and URL */}
            <Box
                display="flex"
                alignItems="center"
                gap={3}
                flexWrap="wrap"
            >
                {article.date && (
                    <Box display="flex" alignItems="center" gap={0.5} sx={{ color: "text.secondary" }}>
                        <CalendarTodayOutlinedIcon sx={{ fontSize: 16 }} />
                        <Typography variant="body2" sx={{ color: "text.secondary" }}>
                            {formatDate(article.date)}
                        </Typography>
                    </Box>
                )}

                {article.url && (
                    <Link
                        href={article.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        underline="hover"
                        onClick={(e) => e.stopPropagation()}
                        sx={{
                            display: "flex",
                            alignItems: "center",
                            gap: 0.5,
                            fontSize: "0.875rem",
                            color: "primary.main",
                        }}
                    >
                        <OpenInNewIcon sx={{ fontSize: 16 }} />
                        {article.url}
                    </Link>
                )}
            </Box>
        </Paper>
    );
}
