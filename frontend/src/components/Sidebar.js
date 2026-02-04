import React from 'react';
import { Link } from 'react-router-dom';

function Sidebar({ categories, loading }) {
  if (loading) {
    return (
      <aside className="sidebar">
        <h3>Categories</h3>
        <div className="loading">Loading categories...</div>
      </aside>
    );
  }

  return (
    <aside className="sidebar">
      <h3>Categories</h3>
      <ul className="category-list">
        {categories && categories.length > 0 ? (
          categories.map(category => (
            <li key={category.id} className="category-item">
              <Link to={`/category/${category.slug}`} className="category-link">
                {category.name}
              </Link>
            </li>
          ))
        ) : (
          <li className="no-categories">No categories yet</li>
        )}
      </ul>
    </aside>
  );
}

export default Sidebar;
