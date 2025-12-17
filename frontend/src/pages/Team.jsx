import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { Users, Award, Zap, Heart } from 'lucide-react'
import axios from 'axios'
import TeamMemberList from '../components/TeamMemberList'
import './Team.css'

function Team() {
  const [members, setMembers] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchTeamMembers()
  }, [])

  const fetchTeamMembers = async () => {
    try {
      const response = await axios.get('http://localhost:8080/api/players')
      // Transform backend data to match frontend expectations
      const positionMap = {
        'goalkeeper': '골키퍼',
        'defender': '수비수',
        'midfielder': '미드필더',
        'forward': '공격수'
      }
      const transformedMembers = response.data.map(player => ({
        id: player.id,
        name: player.name,
        position: positionMap[player.position.toLowerCase()] || player.position,
        number: player.jersey_number || 0,
        role: positionMap[player.position.toLowerCase()] || player.position,
        joinedYear: player.join_date ? new Date(player.join_date).getFullYear() : new Date().getFullYear(),
        stats: {
          matches: player.matches_played || 0,
          goals: player.goals || 0,
          assists: player.assists || 0
        }
      }))
      setMembers(transformedMembers)
      setLoading(false)
    } catch (err) {
      const errorMessage = err.response?.data?.detail || 'Failed to load team members'
      setError(errorMessage)
      setLoading(false)

      setMembers([
        {
          id: 1,
          name: 'Kim Min-jae',
          position: 'Goalkeeper',
          number: 1,
          role: 'Captain',
          joinedYear: 2020,
          stats: { matches: 45, saves: 120 }
        },
        {
          id: 2,
          name: 'Park Ji-sung',
          position: 'Midfielder',
          number: 7,
          role: 'Vice Captain',
          joinedYear: 2020,
          stats: { matches: 43, goals: 15 }
        },
        {
          id: 3,
          name: 'Son Heung-min',
          position: 'Forward',
          number: 10,
          role: 'Striker',
          joinedYear: 2021,
          stats: { matches: 38, goals: 28 }
        },
        {
          id: 4,
          name: 'Lee Kang-in',
          position: 'Midfielder',
          number: 18,
          role: 'Playmaker',
          joinedYear: 2021,
          stats: { matches: 35, assists: 22 }
        },
        {
          id: 5,
          name: 'Hwang Ui-jo',
          position: 'Forward',
          number: 9,
          role: 'Striker',
          joinedYear: 2022,
          stats: { matches: 30, goals: 18 }
        },
        {
          id: 6,
          name: 'Jung Woo-young',
          position: 'Defender',
          number: 4,
          role: 'Center Back',
          joinedYear: 2020,
          stats: { matches: 42, tackles: 95 }
        }
      ])
    }
  }

  const positions = [
    { name: '골키퍼', icon: <Award />, color: '#f093fb' },
    { name: '수비수', icon: <Zap />, color: '#667eea' },
    { name: '미드필더', icon: <Heart />, color: '#4facfe' },
    { name: '공격수', icon: <Users />, color: '#00ff87' }
  ]

  const filteredMembers = (position) => {
    return members.filter(member => member.position === position)
  }

  return (
    <div className="team-page">
      <section className="team-hero">
        <motion.div
          className="team-hero-content"
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
        >
          <h1 className="team-hero-title">
            우리 <span className="gradient-text">팀원들</span>
          </h1>
          <p className="team-hero-subtitle">
            FC쏘아를 빛내는 열정 넘치는 선수들을 소개합니다
          </p>
        </motion.div>
      </section>

      {loading ? (
        <div className="loading-container">
          <div className="loading-spinner" />
          <p>팀원 정보를 불러오는 중...</p>
        </div>
      ) : (
        <>
          {positions.map((position, idx) => {
            const positionMembers = filteredMembers(position.name)
            if (positionMembers.length === 0) return null

            return (
              <section key={position.name} className="position-section">
                <motion.div
                  className="position-header"
                  initial={{ opacity: 0, x: -30 }}
                  whileInView={{ opacity: 1, x: 0 }}
                  viewport={{ once: true }}
                  transition={{ duration: 0.6 }}
                >
                  <div className="position-icon" style={{ color: position.color }}>
                    {position.icon}
                  </div>
                  <h2 className="position-title">{position.name}s</h2>
                </motion.div>

                <TeamMemberList
                  members={positionMembers}
                  position={position.name}
                  positionColor={position.color}
                />
              </section>
            )
          })}

          <section className="team-values">
            <motion.h2
              className="values-title"
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6 }}
            >
              우리 팀의 <span className="gradient-text">가치</span>
            </motion.h2>

            <div className="values-grid">
              {[
                { title: '헌신', description: '비가 오나 눈이 오나, 언제나 그라운드 위에' },
                { title: '팀워크', description: '함께라면 혼자보다 더 강합니다' },
                { title: '최고를 향해', description: '항상 최선을 다합니다' },
                { title: '존중', description: '경기, 상대팀, 그리고 서로를 존중합니다' }
              ].map((value, index) => (
                <motion.div
                  key={index}
                  className="value-card"
                  initial={{ opacity: 0, scale: 0.9 }}
                  whileInView={{ opacity: 1, scale: 1 }}
                  viewport={{ once: true }}
                  transition={{ delay: index * 0.1, duration: 0.5 }}
                  whileHover={{ scale: 1.05 }}
                >
                  <h3 className="value-title">{value.title}</h3>
                  <p className="value-description">{value.description}</p>
                </motion.div>
              ))}
            </div>
          </section>
        </>
      )}
    </div>
  )
}

export default Team
