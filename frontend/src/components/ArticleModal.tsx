import React from 'react';
import type {Article} from '../types/article';

interface ArticleModalProps {
    article: Article | null;
    isOpen: boolean;
    onClose: () => void;
}

const ArticleModal: React.FC<ArticleModalProps> = ({ article, isOpen, onClose }) => {
    if (!isOpen || !article) return null;

    return (
        <div className="modal-overlay" onClick={onClose}>
            <div className="modal-content" onClick={(e) => e.stopPropagation()}>
                <div className="modal-header">
                    <h2 className="modal-title">{article.name}</h2>
                    <button className="modal-close" onClick={onClose}>
                        ✕
                    </button>
                </div>

                <div className="modal-body">
                    <div className="article-full-content">
                        <p>{article.abstract}</p>
                    </div>

                    <div className="article-actions">
                        <a
                            href={article.url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="btn-primary"
                        >
                            View Full Article on Wikipedia
                        </a>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ArticleModal;
