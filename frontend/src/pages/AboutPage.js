import React, { useEffect, useState } from 'react';
import api from '../services/api';

function AboutPage() {
  const [about, setAbout] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAbout = async () => {
      try {
        const response = await api.get('/about');
        setAbout(response.data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchAbout();
  }, []);

  if (loading) {
    return <div className="container loading">Loading...</div>;
  }

  return (
    <div className="container">
      <div className="about-page">
        <h1>{about?.title || 'About'}</h1>
        <div 
          className="about-content" 
          dangerouslySetInnerHTML={{ __html: about?.content_html || '' }}
        />
      </div>
    </div>
  );
}

export default AboutPage;
