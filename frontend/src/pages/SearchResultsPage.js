import React, { useEffect, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import PostCard from '../components/PostCard';
import api from '../services/api';

function SearchResultsPage() {
  const [searchParams] = useSearchParams();
  const query = searchParams.get('q') || '';
  
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchResults = async () => {
      if (!query.trim()) {
        setResults([]);
        setLoading(false);
        return;
      }

      try {
        setLoading(true);
        const response = await api.get(`/search?q=${encodeURIComponent(query)}&limit=20`);
        setResults(response.data.posts || []);
      } catch (err) {
        setError('Search failed');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchResults();
  }, [query]);

  return (
    <div className="container">
      <div className="search-results-page">
        <h1 className="page-title">
          Search Results for "{query}"
        </h1>
        
        {loading ? (
          <div className="loading">Searching...</div>
        ) : error ? (
          <div className="error">{error}</div>
        ) : (
          <>
            <p className="results-count">
              Found {results.length} {results.length === 1 ? 'result' : 'results'}
            </p>
            
            <div className="posts-list">
              {results.length > 0 ? (
                results.map(post => (
                  <PostCard key={post.id} post={post} />
                ))
              ) : (
                <p className="no-results">
                  No posts found matching your search.
                  Try different keywords or <a href="/">browse all posts</a>.
                </p>
              )}
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default SearchResultsPage;
