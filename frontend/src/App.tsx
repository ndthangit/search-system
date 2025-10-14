import { useState } from 'react';
import type {Article} from './types/article';
import { searchArticles } from './services/api';
import SearchBar from './components/SearchBar';
import ArticleList from './components/ArticleList';
import ArticleModal from './components/ArticleModal';
import './App.css';

function App() {
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
      const results = await searchArticles({
        query,
      });

      setArticles(results.list_docs || []);
    } catch (err) {
      setError('Failed to search articles. Please check if the backend is running on localhost:8001');
      console.error('Search error:', err);
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
    <div className="app">
      <header className="app-header">
        <h1>Article Search System</h1>
        <p>Search through Wikipedia articles using our intelligent search system</p>
      </header>

      <main className="app-main">
        <SearchBar onSearch={handleSearch} loading={loading} />

        {error && (
          <div className="error-message">
            <p>{error}</p>
            <p>Make sure your backend is running on localhost:8001</p>
          </div>
        )}

        <ArticleList
          articles={articles}
          loading={loading}
          onArticleClick={handleArticleClick}
        />
      </main>

      <ArticleModal
        article={selectedArticle}
        isOpen={isModalOpen}
        onClose={handleCloseModal}
      />
    </div>
  );
}

export default App
