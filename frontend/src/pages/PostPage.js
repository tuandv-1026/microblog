import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import api from '../services/api';

function PostPage() {
  const { slug } = useParams();
  const [post, setPost] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchPost = async () => {
      try {
        const response = await api.get(`/posts/${slug}`);
        setPost(response.data);
      } catch (err) {
        setError('Post not found');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchPost();
  }, [slug]);

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
                <span key={cat.id} className="category-tag">{cat.name}</span>
              ))}
            </div>
          )}
        </div>
        
        <div className="post-content">
          <div dangerouslySetInnerHTML={{ __html: post.content_html }} />
        </div>
        
        <div className="post-reactions">
          <button className="reaction-btn">👍 Like</button>
          <button className="reaction-btn">❤️ Love</button>
          <button className="reaction-btn">😄 Haha</button>
          <button className="reaction-btn">😮 Wow</button>
        </div>
        
        <div className="comments-section">
          <h3>Comments</h3>
          <form className="comment-form">
            <input type="text" placeholder="Your name" required />
            <input type="email" placeholder="Your email" required />
            <textarea placeholder="Your comment" rows="4" required></textarea>
            <button type="submit">Post Comment</button>
          </form>
        </div>
      </article>
    </div>
  );
}

export default PostPage;
