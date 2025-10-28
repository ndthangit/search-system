import type { Article } from "../types/article";
import ArticleCard from "./ArticleCard";
import {
    Box,
    Typography,
    CircularProgress,
} from "@mui/material";
import Grid from "@mui/material/Grid";

interface ArticleListProps {
    articles: Article[];
    loading: boolean;
    onArticleClick?: (article: Article) => void;
}

export default function ArticleList({ articles, loading, onArticleClick }: ArticleListProps) {
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
                    Searching articles...
                </Typography>
            </Box>
        );
    }

    if (articles.length === 0) {
        return (
            <Box
                sx={{
                    textAlign: "center",
                    p: 4,
                    mt: 3,
                }}
            >
                <Typography variant="h6" gutterBottom>
                    No articles found
                </Typography>
                <Typography variant="body2" color="text.secondary">
                    Try searching for something else.
                </Typography>
            </Box>
        );
    }

    return (
        <Box mt={3}>
            <Typography variant="subtitle1" color="text.secondary" mb={2}>
                Found {articles.length} result{articles.length !== 1 ? "s" : ""}
            </Typography>

            <Grid container spacing={2}>
                {articles.map((article, index) => (
                    <Grid key={index} size={{ xs: 12, sm: 6, md: 4 }}>
                        <ArticleCard article={article} onClick={onArticleClick} />
                    </Grid>
                ))}
            </Grid>
        </Box>
    );
}
