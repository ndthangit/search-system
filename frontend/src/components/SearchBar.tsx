import React, { useState } from 'react';

interface SearchBarProps {
    onSearch: (query: string) => void;
    loading: boolean;
}

const SearchBar: React.FC<SearchBarProps> = ({ onSearch, loading }) => {
    const [query, setQuery] = useState('');

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (query.trim()) {
            onSearch(query.trim());
        }
    };

    const handleClear = () => {
        setQuery('');
        onSearch('');
    };

    return (
        <div className="search-bar">
            <form onSubmit={handleSubmit} className="search-form">
                <div className="search-input-container">
                    <input
                        type="text"
                        value={query}
                        onChange={(e) => setQuery(e.target.value)}
                        placeholder="Search articles..."
                        className="search-input"
                        disabled={loading}
                    />
                    <button
                        type="button"
                        onClick={handleClear}
                        className="clear-button"
                        disabled={loading || !query}
                        title="Clear search"
                    >
                        ✕
                    </button>
                </div>
                <button
                    type="submit"
                    className="search-button"
                    disabled={loading || !query.trim()}
                >
                    {loading ? 'Searching...' : 'Search'}
                </button>
            </form>
        </div>
    );
};

export default SearchBar;
