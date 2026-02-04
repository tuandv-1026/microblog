import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

function PostCard({ post }) {
  return (
    <article className="post-card">
      <h2 className="post-title">
        <a href={`/post/${post.slug}`}>{post.title}</a>
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
      
      <div className="post-excerpt">
        {post.excerpt || 'No excerpt available...'}
      </div>
      
      <a href={`/post/${post.slug}`} className="read-more">
        Read more →
      </a>
    </article>
  );
}

export default PostCard;
