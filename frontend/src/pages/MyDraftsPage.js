import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import api from '../services/api';

function MyDraftsPage() {
  const navigate = useNavigate();
  const [drafts, setDrafts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadDrafts();
  }, []);

  const loadDrafts = async () => {
    try {
      setLoading(true);
      const response = await api.get('/posts?status=draft');
      setDrafts(response.data.items || response.data);
    } catch (err) {
      setError('Failed to load drafts');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (postId, postTitle) => {
    if (!window.confirm(`Delete draft "${postTitle}"?`)) {
      return;
    }

    try {
      await api.delete(`/posts/${postId}`);
      setDrafts(drafts.filter(d => d.id !== postId));
    } catch (err) {
      alert('Failed to delete draft');
    }
  };

  const handlePublish = async (postId, postSlug) => {
    if (!window.confirm('Publish this draft?')) {
      return;
    }

    try {
      await api.post(`/posts/${postId}/publish`);
      navigate(`/posts/${encodeURIComponent(postSlug)}`);
    } catch (err) {
      alert('Failed to publish draft');
    }
  };

  if (loading) {
    return (
      <div className="container">
        <h1>My Drafts</h1>
        <p>Loading drafts...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container">
        <h1>My Drafts</h1>
        <div className="error-message">{error}</div>
      </div>
    );
  }

  return (
    <div className="container">
      <div className="drafts-page">
        <div className="drafts-header">
          <h1>My Drafts</h1>
          <Link to="/posts/new" className="btn-primary">
            New Post
          </Link>
        </div>

        {drafts.length === 0 ? (
          <div className="empty-state">
            <p>No drafts yet.</p>
            <Link to="/posts/new" className="btn-primary">
              Create Your First Post
            </Link>
          </div>
        ) : (
          <div className="drafts-list">
            {drafts.map((draft) => (
              <div key={draft.id} className="draft-card">
                <div className="draft-content">
                  <h2>{draft.title}</h2>
                  {draft.excerpt && <p className="excerpt">{draft.excerpt}</p>}
                  <div className="draft-meta">
                    <span className="meta-item">
                      Created: {new Date(draft.created_at).toLocaleDateString()}
                    </span>
                    <span className="meta-item">
                      Updated: {new Date(draft.updated_at).toLocaleDateString()}
                    </span>
                    {draft.categories && draft.categories.length > 0 && (
                      <span className="meta-item">
                        Categories: {draft.categories.map(c => c.name).join(', ')}
                      </span>
                    )}
                  </div>
                </div>
                <div className="draft-actions">
                  <Link
                    to={`/posts/${draft.id}/edit`}
                    className="btn-secondary"
                  >
                    Edit
                  </Link>
                  <button
                    className="btn-primary"
                    onClick={() => handlePublish(draft.id, draft.slug)}
                  >
                    Publish
                  </button>
                  <button
                    className="btn-danger"
                    onClick={() => handleDelete(draft.id, draft.title)}
                  >
                    Delete
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default MyDraftsPage;
