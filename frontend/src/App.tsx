import { useState } from 'react';
import type {Article, SearchResponse} from './types/article';
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
  const [searchResults, setSearchResults] = useState<SearchResponse | null>(null);
  const [currentPage, setCurrentPage] = useState(1);

  const handleSearch = async (query: string) => {
    if (!query.trim()) {
      setArticles([]);
      setSearchResults(null);
      setError(null);
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const results = await searchArticles({
        query,
        page: currentPage,
        limit: 10,
      });

      setArticles(results.articles);
      setSearchResults(results);
    } catch (err) {
      setError('Failed to search articles. Please check if the backend is running on localhost:8001');
      console.error('Search error:', err);
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

  const handlePageChange = (page: number) => {
    setCurrentPage(page);
    // Re-trigger search with new page
    if (searchResults) {
      handleSearch(searchResults.articles[0]?.title || '');
    }
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>Article Search System</h1>
        <p>Search through articles using our intelligent search system</p>
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
          total={searchResults?.total}
          currentPage={currentPage}
          onPageChange={handlePageChange}
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
