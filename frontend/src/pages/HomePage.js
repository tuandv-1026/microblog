import React, { useEffect, useState } from 'react';
import PostCard from '../components/PostCard';
import api from '../services/api';

function HomePage() {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchPosts = async () => {
      try {
        const response = await api.get('/posts?status=published&limit=20');
        setPosts(response.data);
      } catch (err) {
        setError('Failed to load posts');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchPosts();
  }, []);

  if (loading) {
    return <div className="container loading">Loading posts...</div>;
  }

  if (error) {
    return <div className="container error">{error}</div>;
  }

  return (
    <div className="container">
      <div className="home-page">
        <h1 className="page-title">Latest Posts</h1>
        
        <div className="posts-grid">
          {posts.length > 0 ? (
            posts.map(post => (
              <PostCard key={post.id} post={post} />
            ))
          ) : (
            <p>No posts yet. Check back soon!</p>
          )}
        </div>
      </div>
    </div>
  );
}

export default HomePage;
