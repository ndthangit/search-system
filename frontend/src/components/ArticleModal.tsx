import React from 'react';
import type {Article} from '../types/article';

interface ArticleModalProps {
    article: Article | null;
    isOpen: boolean;
    onClose: () => void;
}

const ArticleModal: React.FC<ArticleModalProps> = ({ article, isOpen, onClose }) => {
    if (!isOpen || !article) return null;

    const formatDate = (dateString: string) => {
        return new Date(dateString).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
        });
    };

    return (
        <div className="modal-overlay" onClick={onClose}>
            <div className="modal-content" onClick={(e) => e.stopPropagation()}>
                <div className="modal-header">
                    <h2 className="modal-title">{article.title}</h2>
                    <button className="modal-close" onClick={onClose}>
                        ✕
                    </button>
                </div>

                <div className="modal-body">
                    <div className="article-meta">
                        <span className="article-author">By {article.author}</span>
                        <span className="article-date">{formatDate(article.publishedAt)}</span>
                    </div>

                    {article.tags && article.tags.length > 0 && (
                        <div className="article-tags">
                            {article.tags.map((tag, index) => (
                                <span key={index} className="tag">
                                    {tag}
                                </span>
                            ))}
                        </div>
                    )}

                    <div className="article-full-content">
                        {article.content}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ArticleModal;
