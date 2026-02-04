import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';

function CreatePostPage() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    title: '',
    slug: '',
    content_markdown: '',
  });
  const [error, setError] = useState('');

  const handleTitleChange = (title) => {
    const slug = title.toLowerCase().replace(/\s+/g, '-').replace(/[^a-z0-9-]/g, '');
    setFormData({ ...formData, title, slug });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    try {
      const response = await api.post('/posts', formData);
      navigate(`/post/${response.data.slug}`);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to create post');
    }
  };

  return (
    <div className="container">
      <div className="create-post-page">
        <h1>Create New Post</h1>
        
        {error && <div className="error-message">{error}</div>}
        
        <form onSubmit={handleSubmit} className="post-form">
          <div className="form-group">
            <label>Title</label>
            <input
              type="text"
              value={formData.title}
              onChange={(e) => handleTitleChange(e.target.value)}
              required
            />
          </div>
          
          <div className="form-group">
            <label>Slug</label>
            <input
              type="text"
              value={formData.slug}
              onChange={(e) => setFormData({ ...formData, slug: e.target.value })}
              required
            />
          </div>
          
          <div className="form-group">
            <label>Content (Markdown)</label>
            <textarea
              value={formData.content_markdown}
              onChange={(e) => setFormData({ ...formData, content_markdown: e.target.value })}
              rows="20"
              required
              placeholder="Write your post in Markdown..."
            ></textarea>
          </div>
          
          <div className="form-actions">
            <button type="submit" className="btn-primary">Create Draft</button>
            <button type="button" className="btn-secondary" onClick={() => navigate('/')}>
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default CreatePostPage;
