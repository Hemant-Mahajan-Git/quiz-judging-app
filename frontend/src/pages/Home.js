import React from 'react';
import './Home.css';

function Home() {
  return (
    <div className="Home">
      <section className="intro">
        <h2>Welcome to Quiz Judging App</h2>
        <p>A comprehensive platform for managing and judging quiz competitions.</p>
      </section>

      <section className="features">
        <h3>Features</h3>
        <div className="features-grid">
          <div className="feature-card">
            <h4>📝 Create Quizzes</h4>
            <p>Easily create and manage quiz content</p>
          </div>
          <div className="feature-card">
            <h4>⭐ Judge Responses</h4>
            <p>Evaluate and score participant answers</p>
          </div>
          <div className="feature-card">
            <h4>📊 Analytics</h4>
            <p>View detailed statistics and performance reports</p>
          </div>
          <div className="feature-card">
            <h4>👥 Team Management</h4>
            <p>Manage judges and participants</p>
          </div>
        </div>
      </section>

      <section className="cta">
        <h3>Getting Started</h3>
        <p>Navigate to the menu to start creating quizzes or managing judgments.</p>
      </section>
    </div>
  );
}

export default Home;
