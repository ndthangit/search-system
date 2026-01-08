import type { Article } from "../types/article";
import ArticleCard from "./ArticleCard";
import {
    Box,
    Typography,
    CircularProgress,
} from "@mui/material";
import AccessTimeIcon from "@mui/icons-material/AccessTime";

interface ArticleListProps {
    articles: Article[];
    loading: boolean;
    onArticleClick?: (article: Article) => void;
    totalResults?: number;
    searchTime?: number | null;
}

export default function ArticleList({
    articles,
    loading,
    onArticleClick,
    totalResults,
    searchTime,
}: ArticleListProps) {
    if (loading) {
        return (
            <Box
                display="flex"
                flexDirection="column"
                alignItems="center"
                justifyContent="center"
                my={5}
            >
                <CircularProgress />
                <Typography variant="body1" sx={{ mt: 2 }}>
                    Đang tìm kiếm...
                </Typography>
            </Box>
        );
    }

    if (totalResults === undefined) {
        return null;
    }

    return (
        <Box>
            {/* Results Header */}
            <Box
                display="flex"
                justifyContent="space-between"
                alignItems="center"
                mb={2}
            >
                <Typography variant="body1" color="text.secondary">
                    Tìm thấy{" "}
                    <Box component="span" fontWeight={600} color="text.primary">
                        {totalResults || articles.length}
                    </Box>{" "}
                    kết quả
                </Typography>

                {searchTime !== null && searchTime !== undefined && (
                    <Box display="flex" alignItems="center" gap={0.5} color="text.secondary">
                        <AccessTimeIcon sx={{ fontSize: 18 }} />
                        <Typography variant="body2">
                            {searchTime}ms
                        </Typography>
                    </Box>
                )}
            </Box>

            {/* Article List */}
            <Box>
                {articles.map((article, index) => (
                    <ArticleCard
                        key={article.id || index}
                        article={article}
                        onClick={onArticleClick}
                    />
                ))}
            </Box>
        </Box>
    );
}
