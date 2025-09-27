import React from 'react';
import type { Article } from '../types/article';

interface ArticleCardProps {
    article: Article;
    onClick?: (article: Article) => void;
}

const ArticleCard: React.FC<ArticleCardProps> = ({ article, onClick }) => {
    const formatDate = (dateString: string) => {
        return new Date(dateString).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
        });
    };

    const truncateContent = (content: string, maxLength: number = 200) => {
        if (content.length <= maxLength) return content;
        return content.substring(0, maxLength) + '...';
    };

    return (
        <div
            className="article-card"
            onClick={() => onClick?.(article)}
        >
            <div className="article-header">
                <h3 className="article-title">{article.title}</h3>
                <div className="article-meta">
                    <span className="article-author">By {article.author}</span>
                    <span className="article-date">{formatDate(article.publishedAt)}</span>
                </div>
            </div>

            {article.summary && (
                <p className="article-summary">{article.summary}</p>
            )}

            <p className="article-content">
                {truncateContent(article.content)}
            </p>

            {article.tags && article.tags.length > 0 && (
                <div className="article-tags">
                    {article.tags.map((tag, index) => (
                        <span key={index} className="tag">
                            {tag}
                        </span>
                    ))}
                </div>
            )}
        </div>
    );
};

export default ArticleCard;
