import React from 'react';
import { Link } from 'react-router-dom';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

function PostCard({ post }) {
  // Create excerpt from HTML content if excerpt is not available
  const getExcerpt = () => {
    if (post.excerpt) {
      return post.excerpt;
    }
    // Extract first 150 chars from HTML content
    const tempDiv = document.createElement('div');
    tempDiv.innerHTML = post.content_html;
    const textContent = tempDiv.textContent || tempDiv.innerText || '';
    return textContent.substring(0, 150) + (textContent.length > 150 ? '...' : '');
  };

  // Reaction emoji mapping
  const reactionEmojis = {
    'like': '👍',
    'love': '❤️',
    'haha': '😄',
    'wow': '😮',
    'sad': '😢',
    'angry': '😠',
  };

  // Format view count
  const formatViews = (count) => {
    if (!count) return '0';
    if (count >= 1000000) return `${(count / 1000000).toFixed(1)}M`;
    if (count >= 1000) return `${(count / 1000).toFixed(1)}K`;
    return count.toString();
  };

  return (
    <article className="post-card">
      <h2 className="post-title">
        <Link to={`/posts/${encodeURIComponent(post.slug)}`}>{post.title}</Link>
      </h2>
      
      <div className="post-meta">
        <span className="post-date">
          {new Date(post.published_at || post.created_at).toLocaleDateString()}
        </span>
        {post.categories && post.categories.length > 0 && (
          <span className="post-categories">
            {post.categories.map(cat => (
              <span key={cat.id} className="category-tag">{cat.name}</span>
            ))}
          </span>
        )}
      </div>
      
      <div 
        className="post-excerpt"
        dangerouslySetInnerHTML={{ 
          __html: post.excerpt 
            ? post.excerpt 
            : (post.content_html.substring(0, 200) + (post.content_html.length > 200 ? '...' : ''))
        }}
      />
      
      <div className="post-stats">
        <span className="stat-item comments">
          <span role="img" aria-label="comments">💬</span>
          <span>{post.comment_count || 0}</span>
        </span>
        {post.reaction_summary && Object.keys(post.reaction_summary).length > 0 ? (
          Object.entries(post.reaction_summary).map(([type, count]) => (
            <span key={type} className="stat-item reactions">
              <span role="img" aria-label={type}>{reactionEmojis[type] || '👍'}</span>
              <span>{count}</span>
            </span>
          ))
        ) : (
          <span className="stat-item reactions">
            <span role="img" aria-label="reactions">❤️</span>
            <span>0</span>
          </span>
        )}
        <span className="stat-item views">
          <span>{formatViews(post.view_count)} views</span>
        </span>
      </div>
      
      <Link to={`/posts/${encodeURIComponent(post.slug)}`} className="read-more">
        Read more →
      </Link>
    </article>
  );
}

export default PostCard;
