import { useState } from "react";

import {
    Container,
    Typography,
    Box,
    Alert,
    CircularProgress,
} from "@mui/material";
import type {Article} from "../../types/article.ts";
import {searchArticles} from "../../services/api.ts";
import ArticleModal from "../../components/ArticleModal.tsx";
import ArticleList from "../../components/ArticleList.tsx";
import SearchBar from "../../components/SearchBar.tsx";

export default function Search() {
    const [articles, setArticles] = useState<Article[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [selectedArticle, setSelectedArticle] = useState<Article | null>(null);
    const [isModalOpen, setIsModalOpen] = useState(false);

    const handleSearch = async (query: string) => {
        if (!query.trim()) {
            setArticles([]);
            setError(null);
            return;
        }

        setLoading(true);
        setError(null);

        try {
            const results = await searchArticles({ query });
            setArticles(results.list_docs || []);
        } catch (err) {
            setError(
                "Failed to search articles. Please check if the backend is running on localhost:8001"
            );
            console.error("Search error:", err);
            setArticles([]);
        } finally {
            setLoading(false);
        }
    };

    const handleArticleClick = (article: Article) => {
        setSelectedArticle(article);
        setIsModalOpen(true);
    };

    const handleCloseModal = () => {
        setIsModalOpen(false);
        setSelectedArticle(null);
    };

    return (
        <Container maxWidth="md" sx={{ py: 4 }}>
            <Box
                sx={{
                    p: 3,
                    textAlign: "center",
                    borderRadius: 3,
                    mb: 4,
                }}
            >
                <Typography variant="h4" gutterBottom fontWeight={600}>
                    Article Search System
                </Typography>
                <Typography variant="subtitle1" color="text.secondary">
                    Search through Wikipedia articles using our intelligent search system
                </Typography>
            </Box>

            <Box sx={{ mb: 3 }}>
                <SearchBar onSearch={handleSearch} loading={loading} />
            </Box>

            {error && (
                <Alert severity="error" sx={{ mb: 3 }}>
                    {error}
                </Alert>
            )}

            {loading && (
                <Box display="flex" justifyContent="center" my={4}>
                    <CircularProgress />
                </Box>
            )}

            {!loading && (
                <ArticleList
                    articles={articles}
                    loading={loading}
                    onArticleClick={handleArticleClick}
                />
            )}

            <ArticleModal
                article={selectedArticle}
                isOpen={isModalOpen}
                onClose={handleCloseModal}
            />
        </Container>
    );
}
