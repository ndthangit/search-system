import React from 'react';
import type {Article} from '../types/article';
import ArticleCard from './ArticleCard';

interface ArticleListProps {
    articles: Article[];
    loading: boolean;
    onArticleClick?: (article: Article) => void;
}

const ArticleList: React.FC<ArticleListProps> = ({
    articles,
    loading,
    onArticleClick,
}) => {
    if (loading) {
        return (
            <div className="article-list loading">
                <div className="loading-spinner"></div>
                <p>Searching articles...</p>
            </div>
        );
    }

    if (articles.length === 0) {
        return (
            <div className="article-list empty">
                <div className="empty-state">
                    <h3>No articles found</h3>
                    <p>Try searching for something else.</p>
                </div>
            </div>
        );
    }

    return (
        <div className="article-list">
            <div className="search-results-header">
                <p>Found {articles.length} result{articles.length !== 1 ? 's' : ''}</p>
            </div>

            <div className="articles-grid">
                {articles.map((article, index) => (
                    <ArticleCard
                        key={index}
                        article={article}
                        onClick={onArticleClick}
                    />
                ))}
            </div>
        </div>
    );
};

export default ArticleList;
