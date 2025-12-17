import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { Trophy, Users, Calendar, Target } from 'lucide-react'
import axios from 'axios'
import './Home.css'

function Home() {
  const [teamStats, setTeamStats] = useState({
    total_matches: 37,
    total_players: 31,
    wins: 16,
    win_rate: 43
  })

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const response = await axios.get('https://fc-ssoa-backend.onrender.com/api/team/stats')
        setTeamStats(response.data)
      } catch (err) {
        console.error('Failed to fetch team stats:', err)
      }
    }
    fetchStats()
  }, [])

  const stats = [
    { icon: <Trophy />, value: teamStats.total_matches, label: '경기 수' },
    { icon: <Users />, value: teamStats.total_players, label: '팀원' },
    { icon: <Target />, value: `${Math.round(teamStats.win_rate)}%`, label: '승률' },
    { icon: <Calendar />, value: '2024', label: '창단년도' }
  ]

  return (
    <div className="home">
      <section className="hero">
        {/* 배경 동영상 */}
        <video
          className="hero-video"
          autoPlay
          muted
          loop
          playsInline
        >
          <source src="/hero-video.mp4" type="video/mp4" />
        </video>
        <div className="hero-overlay" />

        <motion.div
          className="hero-content"
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
        >
          <motion.h1
            className="hero-title"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2, duration: 0.8 }}
          >
            <span className="gradient-text">FC쏘아</span>에 오신 것을 환영합니다
          </motion.h1>
          <motion.p
            className="hero-subtitle"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4, duration: 0.8 }}
          >
            배재고등학교 134기 졸업생일동
          </motion.p>
          <motion.div
            className="hero-cta"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.6, duration: 0.8 }}
          >
            <a href="/gallery" style={{ textDecoration: 'none' }}>
              <button className="cta-primary">하이라이트</button>
            </a>
          </motion.div>
        </motion.div>

        <div className="hero-decoration">
          <div className="floating-ball ball-1">⚽</div>
          <div className="floating-ball ball-2">⚽</div>
          <div className="floating-ball ball-3">⚽</div>
        </div>
      </section>

      <section className="stats-section">
        <div className="stats-container">
          {stats.map((stat, index) => (
            <motion.div
              key={index}
              className="stat-card"
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.1, duration: 0.5 }}
              whileHover={{ y: -10, scale: 1.05 }}
            >
              <div className="stat-icon">{stat.icon}</div>
              <div className="stat-value">{stat.value}</div>
              <div className="stat-label">{stat.label}</div>
            </motion.div>
          ))}
        </div>
      </section>
    </div>
  )
}

export default Home

