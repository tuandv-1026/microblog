import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import PostCard from '../components/PostCard';
import Sidebar from '../components/Sidebar';
import RecentPosts from '../components/RecentPosts';
import api from '../services/api';

function CategoryPage() {
  const { slug } = useParams();
  const [posts, setPosts] = useState([]);
  const [category, setCategory] = useState(null);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        
        // Fetch category details
        const categoryResponse = await api.get(`/categories/${slug}`);
        setCategory(categoryResponse.data);
        
        // Fetch posts in this category
        const postsResponse = await api.get(`/posts?status=published&category_id=${categoryResponse.data.id}&limit=20`);
        setPosts(postsResponse.data);
        
        // Fetch all categories for sidebar
        const categoriesResponse = await api.get('/categories');
        setCategories(categoriesResponse.data);
        
      } catch (err) {
        setError('Failed to load category');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [slug]);

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
            <h1 className="page-title">
              {category ? category.name : 'Category'}
            </h1>
            {category && category.description && (
              <p className="category-description">{category.description}</p>
            )}
          </div>
          
          {loading ? (
            <div className="loading">Loading posts...</div>
          ) : (
            <div className="posts-list">
              {posts.length > 0 ? (
                posts.map(post => (
                  <PostCard key={post.id} post={post} />
                ))
              ) : (
                <p className="no-posts">No posts in this category yet.</p>
              )}
            </div>
          )}
        </main>
        
        {/* Right Column - Categories */}
        <Sidebar categories={categories} loading={loading} />
      </div>
    </div>
  );
}

export default CategoryPage;
