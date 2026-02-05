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
  const [viewMode, setViewMode] = useState('edit'); // 'edit', 'preview', 'split'
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [textareaRef, setTextareaRef] = useState(null);

  // Load categories and post data (if editing)
  useEffect(() => {
    const loadData = async () => {
      try {
        // Load categories
        const categoriesRes = await api.get('/categories');
        setCategories(categoriesRes.data);

        // If editing, load post data
        if (isEditMode) {
          const postRes = await api.get(`/posts/id/${id}`);
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

  const insertMarkdown = (syntax, textBefore = '', textAfter = '') => {
    if (!textareaRef) return;
    
    const start = textareaRef.selectionStart;
    const end = textareaRef.selectionEnd;
    const selectedText = formData.content_markdown.substring(start, end);
    const beforeText = formData.content_markdown.substring(0, start);
    const afterText = formData.content_markdown.substring(end);
    
    let newText;
    let cursorPos;
    
    if (syntax === 'link') {
      newText = `${beforeText}[${selectedText || 'link text'}](url)${afterText}`;
      cursorPos = start + (selectedText ? selectedText.length + 3 : 1);
    } else if (syntax === 'image') {
      newText = `${beforeText}![${selectedText || 'alt text'}](image-url)${afterText}`;
      cursorPos = start + (selectedText ? selectedText.length + 4 : 2);
    } else if (syntax === 'code-block') {
      newText = `${beforeText}\`\`\`\n${selectedText || 'code'}\n\`\`\`${afterText}`;
      cursorPos = start + 4;
    } else if (syntax === 'ul') {
      const lines = (selectedText || 'List item').split('\n');
      const listText = lines.map(line => `- ${line}`).join('\n');
      newText = `${beforeText}${listText}${afterText}`;
      cursorPos = start + listText.length;
    } else if (syntax === 'ol') {
      const lines = (selectedText || 'List item').split('\n');
      const listText = lines.map((line, i) => `${i + 1}. ${line}`).join('\n');
      newText = `${beforeText}${listText}${afterText}`;
      cursorPos = start + listText.length;
    } else if (syntax === 'hr') {
      newText = `${beforeText}\n---\n${afterText}`;
      cursorPos = start + 5;
    } else if (syntax === 'table') {
      const tableText = '\n| Header 1 | Header 2 | Header 3 |\n|----------|----------|----------|\n| Cell 1   | Cell 2   | Cell 3   |\n';
      newText = `${beforeText}${tableText}${afterText}`;
      cursorPos = start + tableText.length;
    } else if (syntax === 'task') {
      newText = `${beforeText}- [ ] ${selectedText || 'Task item'}${afterText}`;
      cursorPos = start + 6 + (selectedText || 'Task item').length;
    } else {
      // For simple wrapping syntax (bold, italic, code, etc.)
      newText = `${beforeText}${textBefore}${selectedText || 'text'}${textAfter}${afterText}`;
      cursorPos = selectedText 
        ? start + textBefore.length + selectedText.length + textAfter.length
        : start + textBefore.length;
    }
    
    setFormData({ ...formData, content_markdown: newText });
    
    // Restore cursor position
    setTimeout(() => {
      textareaRef.focus();
      textareaRef.setSelectionRange(cursorPos, cursorPos);
    }, 0);
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
        navigate(`/posts/${encodeURIComponent(formData.slug)}`);
      } else {
        const response = await api.post('/posts', payload);
        if (status === 'published') {
          navigate(`/posts/${encodeURIComponent(response.data.slug)}`);
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
              className={`btn-toggle ${viewMode === 'edit' ? 'active' : ''}`}
              onClick={() => setViewMode('edit')}
              title="Edit Only"
            >
              ✏️ Edit
            </button>
            <button
              type="button"
              className={`btn-toggle ${viewMode === 'split' ? 'active' : ''}`}
              onClick={() => setViewMode('split')}
              title="Split View"
            >
              Split
            </button>
            <button
              type="button"
              className={`btn-toggle ${viewMode === 'preview' ? 'active' : ''}`}
              onClick={() => setViewMode('preview')}
              title="Preview Only"
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
            {viewMode !== 'preview' && (
              <div className={`form-group ${viewMode === 'split' ? 'editor-split-left' : ''}`}>
                <label>Content (Markdown)</label>
                <div className="markdown-toolbar">
                  <button type="button" className="toolbar-btn" onClick={() => insertMarkdown('h1', '# ', '')} title="Heading 1">
                    <strong>H1</strong>
                  </button>
                  <button type="button" className="toolbar-btn" onClick={() => insertMarkdown('h2', '## ', '')} title="Heading 2">
                    <strong>H2</strong>
                  </button>
                  <button type="button" className="toolbar-btn" onClick={() => insertMarkdown('h3', '### ', '')} title="Heading 3">
                    <strong>H3</strong>
                  </button>
                  <button type="button" className="toolbar-btn" onClick={() => insertMarkdown('h4', '#### ', '')} title="Heading 4">
                    <strong>H4</strong>
                  </button>
                  <button type="button" className="toolbar-btn" onClick={() => insertMarkdown('h5', '##### ', '')} title="Heading 5">
                    <strong>H5</strong>
                  </button>
                  <button type="button" className="toolbar-btn" onClick={() => insertMarkdown('h6', '###### ', '')} title="Heading 6">
                    <strong>H6</strong>
                  </button>
                  <span className="toolbar-divider">|</span>
                  <button type="button" className="toolbar-btn" onClick={() => insertMarkdown('bold', '**', '**')} title="Bold (Ctrl+B)">
                    <strong>B</strong>
                  </button>
                  <button type="button" className="toolbar-btn" onClick={() => insertMarkdown('italic', '*', '*')} title="Italic (Ctrl+I)">
                    <em>I</em>
                  </button>
                  <button type="button" className="toolbar-btn" onClick={() => insertMarkdown('strikethrough', '~~', '~~')} title="Strikethrough">
                    <s>S</s>
                  </button>
                  <span className="toolbar-divider">|</span>
                  <button type="button" className="toolbar-btn toolbar-btn-text" onClick={() => insertMarkdown('ul')} title="Bullet List">
                    UL
                  </button>
                  <button type="button" className="toolbar-btn toolbar-btn-text" onClick={() => insertMarkdown('ol')} title="Numbered List">
                    OL
                  </button>
                  <button type="button" className="toolbar-btn" onClick={() => insertMarkdown('task')} title="Task List">
                    [ ]
                  </button>
                  <button type="button" className="toolbar-btn toolbar-btn-text" onClick={() => insertMarkdown('hr')} title="Horizontal Line">
                    HR
                  </button>
                  <span className="toolbar-divider">|</span>
                  <button type="button" className="toolbar-btn toolbar-btn-text" onClick={() => insertMarkdown('link')} title="Link">
                    Link
                  </button>
                  <button type="button" className="toolbar-btn toolbar-btn-text" onClick={() => insertMarkdown('image')} title="Image">
                    Img
                  </button>
                  <button type="button" className="toolbar-btn toolbar-btn-text" onClick={() => insertMarkdown('table')} title="Table">
                    Table
                  </button>
                  <span className="toolbar-divider">|</span>
                  <button type="button" className="toolbar-btn" onClick={() => insertMarkdown('code', '`', '`')} title="Inline Code">
                    {'<>'}
                  </button>
                  <button type="button" className="toolbar-btn" onClick={() => insertMarkdown('code-block')} title="Code Block">
                    {'{}'}
                  </button>
                  <button type="button" className="toolbar-btn" onClick={() => insertMarkdown('quote', '> ', '')} title="Quote">
                    {'>'}
                  </button>
                </div>
                <textarea
                  ref={setTextareaRef}
                  className="markdown-editor"
                  value={formData.content_markdown}
                  onChange={(e) => setFormData({ ...formData, content_markdown: e.target.value })}
                  rows="25"
                  required
                  placeholder="Write your post in Markdown..."
                ></textarea>
              </div>
            )}
            
            {viewMode !== 'edit' && (
              <div className={`markdown-preview ${viewMode === 'split' ? 'editor-split-right' : ''}`}>
                <div className="preview-header">
                  <label>Preview</label>
                </div>
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
