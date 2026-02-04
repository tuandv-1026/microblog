import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import api from '../services/api';

function CreatePostPage() {
  const navigate = useNavigate();
  const { id } = useParams(); // For edit mode
  const isEditMode = Boolean(id);
  
  const [formData, setFormData] = useState({
    title: '',
    slug: '',
    content_markdown: '',
    excerpt: '',
    category_ids: [],
  });
  const [categories, setCategories] = useState([]);
  const [showPreview, setShowPreview] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  // Load categories and post data (if editing)
  useEffect(() => {
    const loadData = async () => {
      try {
        // Load categories
        const categoriesRes = await api.get('/categories');
        setCategories(categoriesRes.data);

        // If editing, load post data
        if (isEditMode) {
          const postRes = await api.get(`/posts/${id}`);
          const post = postRes.data;
          setFormData({
            title: post.title,
            slug: post.slug,
            content_markdown: post.content_markdown,
            excerpt: post.excerpt || '',
            category_ids: post.categories.map(c => c.id),
          });
        }
      } catch (err) {
        setError('Failed to load data');
      }
    };
    loadData();
  }, [id, isEditMode]);

  const handleTitleChange = (title) => {
    // Auto-generate slug from title (only for new posts)
    if (!isEditMode) {
      const slug = title.toLowerCase()
        .replace(/\s+/g, '-')
        .replace(/[^a-z0-9-]/g, '')
        .replace(/--+/g, '-')
        .replace(/^-|-$/g, '');
      setFormData({ ...formData, title, slug });
    } else {
      setFormData({ ...formData, title });
    }
  };

  const handleCategoryToggle = (categoryId) => {
    const currentIds = formData.category_ids;
    const newIds = currentIds.includes(categoryId)
      ? currentIds.filter(id => id !== categoryId)
      : [...currentIds, categoryId];
    setFormData({ ...formData, category_ids: newIds });
  };

  const handleSubmit = async (status) => {
    setError('');
    setLoading(true);

    try {
      const payload = {
        ...formData,
        status, // 'draft' or 'published'
      };

      if (isEditMode) {
        await api.put(`/posts/${id}`, payload);
        navigate(`/posts/${formData.slug}`);
      } else {
        const response = await api.post('/posts', payload);
        if (status === 'published') {
          navigate(`/posts/${response.data.slug}`);
        } else {
          navigate('/my-drafts');
        }
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to save post');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <div className="editor-page">
        <div className="editor-header">
          <h1>{isEditMode ? 'Edit Post' : 'Create New Post'}</h1>
          <div className="editor-controls">
            <button
              type="button"
              className={`btn-toggle ${!showPreview ? 'active' : ''}`}
              onClick={() => setShowPreview(false)}
            >
              Edit
            </button>
            <button
              type="button"
              className={`btn-toggle ${showPreview ? 'active' : ''}`}
              onClick={() => setShowPreview(true)}
            >
              Preview
            </button>
          </div>
        </div>
        
        {error && <div className="error-message">{error}</div>}
        
        <div className="editor-form">
          <div className="form-group">
            <label>Title</label>
            <input
              type="text"
              value={formData.title}
              onChange={(e) => handleTitleChange(e.target.value)}
              required
              placeholder="Enter post title..."
            />
          </div>
          
          <div className="form-group">
            <label>Slug</label>
            <input
              type="text"
              value={formData.slug}
              onChange={(e) => setFormData({ ...formData, slug: e.target.value })}
              required
              placeholder="url-friendly-slug"
              disabled={isEditMode}
            />
            {!isEditMode && <small className="form-hint">Auto-generated from title. Edit if needed.</small>}
            {isEditMode && <small className="form-hint">Slug cannot be changed after publishing.</small>}
          </div>

          <div className="form-group">
            <label>Excerpt (Optional)</label>
            <textarea
              value={formData.excerpt}
              onChange={(e) => setFormData({ ...formData, excerpt: e.target.value })}
              rows="2"
              placeholder="Brief summary for post cards..."
            ></textarea>
          </div>

          <div className="form-group">
            <label>Categories</label>
            <div className="category-select">
              {categories.map((category) => (
                <label key={category.id} className="category-checkbox">
                  <input
                    type="checkbox"
                    checked={formData.category_ids.includes(category.id)}
                    onChange={() => handleCategoryToggle(category.id)}
                  />
                  <span>{category.name}</span>
                </label>
              ))}
            </div>
          </div>
          
          <div className="editor-content">
            {!showPreview ? (
              <div className="form-group">
                <label>Content (Markdown)</label>
                <textarea
                  className="markdown-editor"
                  value={formData.content_markdown}
                  onChange={(e) => setFormData({ ...formData, content_markdown: e.target.value })}
                  rows="25"
                  required
                  placeholder="Write your post in Markdown...

**Markdown Syntax:**
# Heading 1
## Heading 2
**bold** *italic*
[link](url)
![image](url)
- List item
> Quote
\`code\`
\`\`\`
code block
\`\`\`
"
                ></textarea>
              </div>
            ) : (
              <div className="markdown-preview">
                <label>Preview</label>
                <div className="preview-content">
                  <h1>{formData.title || 'Untitled Post'}</h1>
                  {formData.excerpt && <p className="excerpt">{formData.excerpt}</p>}
                  <ReactMarkdown remarkPlugins={[remarkGfm]}>
                    {formData.content_markdown || '*No content yet...*'}
                  </ReactMarkdown>
                </div>
              </div>
            )}
          </div>
          
          <div className="form-actions">
            <button
              type="button"
              className="btn-secondary"
              onClick={() => handleSubmit('draft')}
              disabled={loading}
            >
              {loading ? 'Saving...' : (isEditMode ? 'Save as Draft' : 'Save Draft')}
            </button>
            <button
              type="button"
              className="btn-primary"
              onClick={() => handleSubmit('published')}
              disabled={loading}
            >
              {loading ? 'Publishing...' : (isEditMode ? 'Update & Publish' : 'Publish')}
            </button>
            <button
              type="button"
              className="btn-cancel"
              onClick={() => navigate(isEditMode ? `/posts/${formData.slug}` : '/')}
              disabled={loading}
            >
              Cancel
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default CreatePostPage;
