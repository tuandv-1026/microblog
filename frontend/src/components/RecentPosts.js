import React from 'react';
import { Link } from 'react-router-dom';

function RecentPosts({ posts, loading }) {
  if (loading) {
    return (
      <aside className="recent-posts">
        <h3>Recent Posts</h3>
        <div className="loading">Loading...</div>
      </aside>
    );
  }

  return (
    <aside className="recent-posts">
      <h3>Recent Posts</h3>
      <ul className="recent-posts-list">
        {posts && posts.length > 0 ? (
          posts.slice(0, 5).map(post => (
            <li key={post.id} className="recent-post-item">
              <Link to={`/post/${post.slug}`} className="recent-post-link">
                <span className="recent-post-title">{post.title}</span>
                <span className="recent-post-date">
                  {new Date(post.published_at || post.created_at).toLocaleDateString()}
                </span>
              </Link>
            </li>
          ))
        ) : (
          <li className="no-posts">No posts yet</li>
        )}
      </ul>
    </aside>
  );
}

export default RecentPosts;
