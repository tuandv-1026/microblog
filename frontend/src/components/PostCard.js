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
      
      <Link to={`/posts/${encodeURIComponent(post.slug)}`} className="read-more">
        Read more →
      </Link>
    </article>
  );
}

export default PostCard;
