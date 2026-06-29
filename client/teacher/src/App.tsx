// import { useState } from 'react'
import { Link, Route, Routes } from 'react-router-dom'
// import reactLogo from './assets/react.svg'
// import viteLogo from './assets/vite.svg'
// import heroImg from './assets/hero.png'
import './App.css'
import LoginPage from './pages/Login'

function HomePage() {
  return (
    <main id="home" className="home-container">
      <div className="home-background"></div>
      <div className="home-content">
        <div className="hero-section">
          <h1 className="brand-title">CleverCheck</h1>
          <p className="brand-subtitle">Intelligent Test Evaluation System</p>
          
          <div className="slogan-container">
            <p className="slogan-hebrew">דיוק של מורה. מהירות של מערכת.</p>
            <p className="slogan-english">The accuracy of a teacher, the speed of a system</p>
          </div>

          <div className="cta-section">
            <p className="login-prompt">Ready to experience smarter grading?</p>
            <Link to="/login" className="login-button">Enter CleverCheck</Link>
          </div>
        </div>
      </div>
    </main>
  )
}

function App() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/login" element={<LoginPage />} />
    </Routes>
  )
}

export default App
