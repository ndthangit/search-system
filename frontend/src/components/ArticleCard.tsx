import React from 'react';
import type { Article } from '../types/article';

interface ArticleCardProps {
    article: Article;
    onClick?: (article: Article) => void;
}

const ArticleCard: React.FC<ArticleCardProps> = ({ article, onClick }) => {
    const truncateAbstract = (abstract: string, maxLength: number = 200) => {
        if (abstract.length <= maxLength) return abstract;
        return abstract.substring(0, maxLength) + '...';
    };

    return (
        <div
            className="article-card"
            onClick={() => onClick?.(article)}
        >
            <div className="article-header">
                <h3 className="article-title">{article.name}</h3>
            </div>

            <p className="article-abstract">
                {truncateAbstract(article.abstract)}
            </p>

            <a
                href={article.url}
                target="_blank"
                rel="noopener noreferrer"
                className="article-link"
                onClick={(e) => e.stopPropagation()}
            >
                Read more on Wikipedia →
            </a>
        </div>
    );
};

export default ArticleCard;
