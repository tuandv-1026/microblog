import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import api from '../services/api';

function PostPage() {
  const { slug } = useParams();
  const [post, setPost] = useState(null);
  const [comments, setComments] = useState([]);
  const [reactions, setReactions] = useState(null);
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  // Comment form state
  const [commentForm, setCommentForm] = useState({
    author_name: '',
    author_email: '',
    content: '',
  });
  const [commentSubmitting, setCommentSubmitting] = useState(false);

  useEffect(() => {
    fetchData();
    checkAuth();
  }, [slug]);

  const checkAuth = async () => {
    try {
      const response = await api.get('/auth/me');
      setUser(response.data);
    } catch (err) {
      setUser(null);
    }
  };

  const fetchData = async () => {
    try {
      setLoading(true);
      
      // Fetch post
      const postResponse = await api.get(`/posts/${slug}`);
      setPost(postResponse.data);
      
      // Fetch comments
      const commentsResponse = await api.get(`/comments/post/${postResponse.data.id}`);
      setComments(commentsResponse.data);
      
      // Fetch reactions
      const reactionsResponse = await api.get(`/reactions/post/${postResponse.data.id}/summary`);
      setReactions(reactionsResponse.data);
      
    } catch (err) {
      setError('Post not found');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleReaction = async (type) => {
    if (!user) {
      alert('Please login to react');
      return;
    }

    try {
      await api.post('/reactions', {
        type: type,
        post_id: post.id,
      });
      
      // Refresh reactions
      const reactionsResponse = await api.get(`/reactions/post/${post.id}/summary`);
      setReactions(reactionsResponse.data);
    } catch (err) {
      console.error('Failed to toggle reaction', err);
    }
  };

  const handleCommentSubmit = async (e) => {
    e.preventDefault();
    
    if (!commentForm.author_name || !commentForm.author_email || !commentForm.content) {
      alert('Please fill in all fields');
      return;
    }

    try {
      setCommentSubmitting(true);
      await api.post('/comments', {
        ...commentForm,
        post_id: post.id,
      });
      
      // Refresh comments
      const commentsResponse = await api.get(`/comments/post/${post.id}`);
      setComments(commentsResponse.data);
      
      // Clear form
      setCommentForm({
        author_name: '',
        author_email: '',
        content: '',
      });
    } catch (err) {
      alert('Failed to post comment');
      console.error(err);
    } finally {
      setCommentSubmitting(false);
    }
  };

  if (loading) {
    return <div className="container loading">Loading post...</div>;
  }

  if (error || !post) {
    return <div className="container error">{error || 'Post not found'}</div>;
  }

  return (
    <div className="container">
      <article className="post-detail">
        <h1 className="post-title">{post.title}</h1>
        
        <div className="post-meta">
          <span className="post-date">
            {new Date(post.published_at || post.created_at).toLocaleDateString('en-US', {
              year: 'numeric',
              month: 'long',
              day: 'numeric'
            })}
          </span>
          {post.categories && post.categories.length > 0 && (
            <div className="post-categories">
              {post.categories.map(cat => (
                <Link 
                  key={cat.id} 
                  to={`/category/${cat.slug}`}
                  className="category-tag"
                >
                  {cat.name}
                </Link>
              ))}
            </div>
          )}
        </div>

        {/* Author Actions */}
        {user && user.id === post.author_id && (
          <div className="post-actions">
            <Link to={`/posts/${post.id}/edit`} className="btn-secondary">
              Edit Post
            </Link>
          </div>
        )}
        
        <div className="post-content">
          <div dangerouslySetInnerHTML={{ __html: post.content_html }} />
        </div>
        
        {/* Reactions */}
        <div className="post-reactions">
          <h3>React to this post</h3>
          <div className="reactions-buttons">
            <button 
              className="reaction-btn" 
              onClick={() => handleReaction('like')}
              disabled={!user}
            >
              👍 Like {reactions && reactions.like > 0 && `(${reactions.like})`}
            </button>
            <button 
              className="reaction-btn" 
              onClick={() => handleReaction('love')}
              disabled={!user}
            >
              ❤️ Love {reactions && reactions.love > 0 && `(${reactions.love})`}
            </button>
            <button 
              className="reaction-btn" 
              onClick={() => handleReaction('haha')}
              disabled={!user}
            >
              😄 Haha {reactions && reactions.haha > 0 && `(${reactions.haha})`}
            </button>
            <button 
              className="reaction-btn" 
              onClick={() => handleReaction('wow')}
              disabled={!user}
            >
              😮 Wow {reactions && reactions.wow > 0 && `(${reactions.wow})`}
            </button>
            <button 
              className="reaction-btn" 
              onClick={() => handleReaction('sad')}
              disabled={!user}
            >
              😢 Sad {reactions && reactions.sad > 0 && `(${reactions.sad})`}
            </button>
            <button 
              className="reaction-btn" 
              onClick={() => handleReaction('angry')}
              disabled={!user}
            >
              😠 Angry {reactions && reactions.angry > 0 && `(${reactions.angry})`}
            </button>
          </div>
          {!user && (
            <p className="login-message">
              <Link to="/login">Login</Link> to react to this post
            </p>
          )}
        </div>
        
        {/* Comments Section */}
        <div className="comments-section">
          <h3>Comments ({comments.length})</h3>
          
          {/* Comment Form */}
          <form className="comment-form" onSubmit={handleCommentSubmit}>
            <div className="form-row">
              <input 
                type="text" 
                placeholder="Your name" 
                value={commentForm.author_name}
                onChange={(e) => setCommentForm({...commentForm, author_name: e.target.value})}
                required 
              />
              <input 
                type="email" 
                placeholder="Your email" 
                value={commentForm.author_email}
                onChange={(e) => setCommentForm({...commentForm, author_email: e.target.value})}
                required 
              />
            </div>
            <textarea 
              placeholder="Your comment" 
              rows="4" 
              value={commentForm.content}
              onChange={(e) => setCommentForm({...commentForm, content: e.target.value})}
              required
            />
            <button type="submit" disabled={commentSubmitting}>
              {commentSubmitting ? 'Posting...' : 'Post Comment'}
            </button>
          </form>
          
          {/* Comments List */}
          <div className="comments-list">
            {comments.length > 0 ? (
              comments.map(comment => (
                <div key={comment.id} className="comment">
                  <div className="comment-header">
                    <strong className="comment-author">{comment.author_name}</strong>
                    <span className="comment-date">
                      {new Date(comment.created_at).toLocaleDateString()}
                    </span>
                  </div>
                  <p className="comment-content">{comment.content}</p>
                </div>
              ))
            ) : (
              <p className="no-comments">No comments yet. Be the first to comment!</p>
            )}
          </div>
        </div>
      </article>
    </div>
  );
}

export default PostPage;
