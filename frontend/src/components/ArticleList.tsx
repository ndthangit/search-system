import React from 'react';
import type {Article} from '../types/article';
import ArticleCard from './ArticleCard';

interface ArticleListProps {
    articles: Article[];
    loading: boolean;
    onArticleClick?: (article: Article) => void;
    total?: number;
    currentPage?: number;
    onPageChange?: (page: number) => void;
}

const ArticleList: React.FC<ArticleListProps> = ({
    articles,
    loading,
    onArticleClick,
    total,
    currentPage = 1,
    onPageChange,
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
                    <p>Try adjusting your search terms or browse all articles.</p>
                </div>
            </div>
        );
    }

    return (
        <div className="article-list">
            {total && (
                <div className="search-results-header">
                    <p>Found {total} article{total !== 1 ? 's' : ''}</p>
                </div>
            )}

            <div className="articles-grid">
                {articles.map((article) => (
                    <ArticleCard
                        key={article.id}
                        article={article}
                        onClick={onArticleClick}
                    />
                ))}
            </div>

            {onPageChange && total && total > 10 && (
                <div className="pagination">
                    <button
                        onClick={() => onPageChange(currentPage - 1)}
                        disabled={currentPage <= 1}
                        className="pagination-button"
                    >
                        Previous
                    </button>
                    <span className="pagination-info">
                        Page {currentPage} of {Math.ceil(total / 10)}
                    </span>
                    <button
                        onClick={() => onPageChange(currentPage + 1)}
                        disabled={currentPage >= Math.ceil(total / 10)}
                        className="pagination-button"
                    >
                        Next
                    </button>
                </div>
            )}
        </div>
    );
};

export default ArticleList;
