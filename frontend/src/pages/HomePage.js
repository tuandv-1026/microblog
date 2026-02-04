import React, { useEffect, useState } from 'react';
import PostCard from '../components/PostCard';
import Sidebar from '../components/Sidebar';
import RecentPosts from '../components/RecentPosts';
import api from '../services/api';

function HomePage() {
  const [posts, setPosts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [sortBy, setSortBy] = useState('newest');
  const [page, setPage] = useState(1);
  const [hasMore, setHasMore] = useState(true);
  const limit = 10;

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        
        // Fetch posts
        const postsResponse = await api.get(
          `/posts?status=published&limit=${limit}&offset=${(page - 1) * limit}`
        );
        setPosts(postsResponse.data);
        setHasMore(postsResponse.data.length === limit);
        
        // Fetch categories
        const categoriesResponse = await api.get('/categories');
        setCategories(categoriesResponse.data);
        
      } catch (err) {
        setError('Failed to load data');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [page, sortBy]);

  const handleSortChange = (newSort) => {
    setSortBy(newSort);
    setPage(1);
  };

  const handleNextPage = () => {
    if (hasMore) {
      setPage(page + 1);
    }
  };

  const handlePrevPage = () => {
    if (page > 1) {
      setPage(page - 1);
    }
  };

  if (error) {
    return <div className="container error">{error}</div>;
  }

  return (
    <div className="container">
      <div className="home-layout">
        {/* Left Column - Recent Posts */}
        <RecentPosts posts={posts} loading={loading} />
        
        {/* Center Column - Main Content */}
        <main className="main-column">
          <div className="page-header">
            <h1 className="page-title">Latest Posts</h1>
            
            <div className="sort-controls">
              <label>Sort by:</label>
              <select 
                value={sortBy} 
                onChange={(e) => handleSortChange(e.target.value)}
                className="sort-select"
              >
                <option value="newest">Newest First</option>
                <option value="oldest">Oldest First</option>
              </select>
            </div>
          </div>
          
          {loading ? (
            <div className="loading">Loading posts...</div>
          ) : (
            <>
              <div className="posts-list">
                {posts.length > 0 ? (
                  posts.map(post => (
                    <PostCard key={post.id} post={post} />
                  ))
                ) : (
                  <p className="no-posts">No posts yet. Check back soon!</p>
                )}
              </div>
              
              {posts.length > 0 && (
                <div className="pagination">
                  <button 
                    onClick={handlePrevPage} 
                    disabled={page === 1}
                    className="btn-pagination"
                  >
                    ← Previous
                  </button>
                  <span className="page-number">Page {page}</span>
                  <button 
                    onClick={handleNextPage} 
                    disabled={!hasMore}
                    className="btn-pagination"
                  >
                    Next →
                  </button>
                </div>
              )}
            </>
          )}
        </main>
        
        {/* Right Column - Categories */}
        <Sidebar categories={categories} loading={loading} />
      </div>
    </div>
  );
}

export default HomePage;
