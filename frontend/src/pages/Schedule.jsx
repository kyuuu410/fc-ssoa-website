import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Calendar, Clock, MapPin, Trophy, TrendingUp, TrendingDown, Minus, Plus, Edit2, Trash2, X, Save, CheckCircle } from 'lucide-react'
import axios from 'axios'
import './Schedule.css'

function Schedule() {
  const [matches, setMatches] = useState([])
  const [players, setPlayers] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [filter, setFilter] = useState('all')
  const [showModal, setShowModal] = useState(false)
  const [showCompleteModal, setShowCompleteModal] = useState(false)
  const [editingMatch, setEditingMatch] = useState(null)
  const [completingMatch, setCompletingMatch] = useState(null)
  const [formData, setFormData] = useState({
    opponent: '',
    match_date: '',
    match_time: '06:00',
    location: '',
    home_away: 'home',
    status: 'scheduled',
    fc_ssoa_score: '',
    opponent_score: ''
  })
  const [completeFormData, setCompleteFormData] = useState({
    fc_ssoa_score: 0,
    opponent_score: 0,
    goals: [],
    assists: []
  })
  const [teamStats, setTeamStats] = useState({ total_matches: 0, wins: 0, draws: 0, losses: 0 })

  useEffect(() => {
    fetchMatches()
    fetchPlayers()
    fetchTeamStats()
  }, [])

  const fetchTeamStats = async () => {
    try {
      const response = await axios.get('http://localhost:8080/api/team/stats')
      setTeamStats(response.data)
    } catch (err) {
      console.error('Failed to fetch team stats:', err)
    }
  }

  const fetchMatches = async () => {
    try {
      const response = await axios.get('http://localhost:8080/api/matches')
      const transformedMatches = response.data.map(match => {
        const matchDateTime = new Date(match.match_date)
        const date = matchDateTime.toISOString().split('T')[0]
        const time = matchDateTime.toTimeString().slice(0, 5)

        let result = null
        let score = null
        let status = match.status === 'scheduled' ? 'upcoming' : match.status

        if (match.status === 'completed' && match.fc_ssoa_score !== null && match.opponent_score !== null) {
          score = {
            home: match.fc_ssoa_score,
            away: match.opponent_score
          }

          if (match.fc_ssoa_score > match.opponent_score) {
            result = 'win'
          } else if (match.fc_ssoa_score < match.opponent_score) {
            result = 'loss'
          } else {
            result = 'draw'
          }
        }

        return {
          id: match.id,
          date,
          time,
          opponent: match.opponent,
          location: match.location,
          home_away: match.home_away,
          status,
          score,
          result
        }
      })
      setMatches(transformedMatches)
      setLoading(false)
    } catch (err) {
      setError('경기 정보를 불러오는데 실패했습니다')
      setLoading(false)
    }
  }

  const fetchPlayers = async () => {
    try {
      const response = await axios.get('http://localhost:8080/api/matches/players-for-stats')
      setPlayers(response.data)
    } catch (err) {
      console.error('Failed to fetch players:', err)
    }
  }

  const resetForm = () => {
    setFormData({
      opponent: '',
      match_date: '',
      match_time: '06:00',
      location: '',
      home_away: 'home',
      status: 'scheduled',
      fc_ssoa_score: '',
      opponent_score: ''
    })
    setEditingMatch(null)
  }

  const openAddModal = () => {
    resetForm()
    setShowModal(true)
  }

  const openEditModal = (match) => {
    setEditingMatch(match)
    setFormData({
      opponent: match.opponent,
      match_date: match.date,
      match_time: match.time,
      location: match.location,
      home_away: match.home_away || 'home',
      status: match.status === 'upcoming' ? 'scheduled' : match.status,
      fc_ssoa_score: match.score?.home ?? '',
      opponent_score: match.score?.away ?? ''
    })
    setShowModal(true)
  }

  const openCompleteModal = (match) => {
    setCompletingMatch(match)
    setCompleteFormData({
      fc_ssoa_score: 0,
      opponent_score: 0,
      goals: [],
      assists: []
    })
    setShowCompleteModal(true)
  }

  const closeModal = () => {
    setShowModal(false)
    resetForm()
  }

  const closeCompleteModal = () => {
    setShowCompleteModal(false)
    setCompletingMatch(null)
    setCompleteFormData({
      fc_ssoa_score: 0,
      opponent_score: 0,
      goals: [],
      assists: []
    })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()

    const matchDateTime = `${formData.match_date}T${formData.match_time}:00`
    const payload = {
      opponent: formData.opponent,
      match_date: matchDateTime,
      location: formData.location,
      home_away: formData.home_away,
      status: formData.status,
      fc_ssoa_score: formData.fc_ssoa_score !== '' ? parseInt(formData.fc_ssoa_score) : null,
      opponent_score: formData.opponent_score !== '' ? parseInt(formData.opponent_score) : null
    }

    try {
      if (editingMatch) {
        await axios.put(`http://localhost:8080/api/matches/${editingMatch.id}`, payload)
      } else {
        await axios.post('http://localhost:8080/api/matches', payload)
      }
      closeModal()
      fetchMatches()
    } catch (err) {
      alert('저장에 실패했습니다: ' + (err.response?.data?.detail || err.message))
    }
  }

  const handleCompleteSubmit = async (e) => {
    e.preventDefault()

    const payload = {
      fc_ssoa_score: completeFormData.fc_ssoa_score,
      opponent_score: completeFormData.opponent_score,
      goals: completeFormData.goals.filter(g => g.player_name),
      assists: completeFormData.assists.filter(a => a.player_name)
    }

    try {
      await axios.post(`http://localhost:8080/api/matches/${completingMatch.id}/complete`, payload)
      closeCompleteModal()
      fetchMatches()
      alert('경기가 완료 처리되었고 선수 통계가 업데이트되었습니다!')
    } catch (err) {
      alert('완료 처리에 실패했습니다: ' + (err.response?.data?.detail || err.message))
    }
  }

  const handleDelete = async (matchId) => {
    if (!confirm('정말 이 경기를 삭제하시겠습니까?')) return

    try {
      await axios.delete(`http://localhost:8080/api/matches/${matchId}`)
      fetchMatches()
    } catch (err) {
      alert('삭제에 실패했습니다: ' + (err.response?.data?.detail || err.message))
    }
  }

  const addGoalEntry = () => {
    setCompleteFormData({
      ...completeFormData,
      goals: [...completeFormData.goals, { player_name: '', count: 1 }]
    })
  }

  const addAssistEntry = () => {
    setCompleteFormData({
      ...completeFormData,
      assists: [...completeFormData.assists, { player_name: '', count: 1 }]
    })
  }

  const updateGoal = (index, field, value) => {
    const newGoals = [...completeFormData.goals]
    newGoals[index][field] = field === 'count' ? parseInt(value) || 1 : value
    setCompleteFormData({ ...completeFormData, goals: newGoals })
  }

  const updateAssist = (index, field, value) => {
    const newAssists = [...completeFormData.assists]
    newAssists[index][field] = field === 'count' ? parseInt(value) || 1 : value
    setCompleteFormData({ ...completeFormData, assists: newAssists })
  }

  const removeGoal = (index) => {
    const newGoals = completeFormData.goals.filter((_, i) => i !== index)
    setCompleteFormData({ ...completeFormData, goals: newGoals })
  }

  const removeAssist = (index) => {
    const newAssists = completeFormData.assists.filter((_, i) => i !== index)
    setCompleteFormData({ ...completeFormData, assists: newAssists })
  }

  const filteredMatches = matches.filter(match => {
    if (filter === 'all') return true
    return match.status === filter
  })

  const getResultIcon = (result) => {
    switch (result) {
      case 'win':
        return <TrendingUp className="result-icon win" />
      case 'loss':
        return <TrendingDown className="result-icon loss" />
      case 'draw':
        return <Minus className="result-icon draw" />
      default:
        return null
    }
  }

  const getResultClass = (result) => {
    return result ? `match-result-${result}` : ''
  }

  const stats = {
    played: teamStats.total_matches,
    won: teamStats.wins,
    drawn: teamStats.draws,
    lost: teamStats.losses
  }

  return (
    <div className="schedule-page">
      <section className="schedule-hero">
        <motion.div
          className="schedule-hero-content"
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
        >
          <h1 className="schedule-hero-title">
            경기 <span className="gradient-text">일정</span>
          </h1>
          <p className="schedule-hero-subtitle">
            FC쏘아의 경기 일정과 결과를 확인하세요
          </p>
        </motion.div>
      </section>

      <section className="stats-overview">
        <div className="stats-cards">
          <motion.div
            className="stat-overview-card"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
          >
            <div className="stat-overview-value">{stats.played}</div>
            <div className="stat-overview-label">경기</div>
          </motion.div>
          <motion.div
            className="stat-overview-card win-card"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
          >
            <div className="stat-overview-value">{stats.won}</div>
            <div className="stat-overview-label">승</div>
          </motion.div>
          <motion.div
            className="stat-overview-card draw-card"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
          >
            <div className="stat-overview-value">{stats.drawn}</div>
            <div className="stat-overview-label">무</div>
          </motion.div>
          <motion.div
            className="stat-overview-card loss-card"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
          >
            <div className="stat-overview-value">{stats.lost}</div>
            <div className="stat-overview-label">패</div>
          </motion.div>
        </div>
      </section>

      <section className="schedule-content">
        <div className="schedule-filters">
          <div className="filter-buttons">
            <button
              className={`filter-btn ${filter === 'all' ? 'active' : ''}`}
              onClick={() => setFilter('all')}
            >
              전체
            </button>
            <button
              className={`filter-btn ${filter === 'upcoming' ? 'active' : ''}`}
              onClick={() => setFilter('upcoming')}
            >
              예정
            </button>
            <button
              className={`filter-btn ${filter === 'completed' ? 'active' : ''}`}
              onClick={() => setFilter('completed')}
            >
              완료
            </button>
          </div>
          <button className="add-match-btn" onClick={openAddModal}>
            <Plus size={20} />
            경기 추가
          </button>
        </div>

        {loading ? (
          <div className="loading-container">
            <div className="loading-spinner" />
            <p>경기 정보를 불러오는 중...</p>
          </div>
        ) : (
          <div className="matches-list">
            {filteredMatches.map((match, index) => (
              <motion.div
                key={match.id}
                className={`match-card ${getResultClass(match.result)} ${match.status === 'upcoming' ? 'upcoming-highlight' : ''}`}
                initial={{ opacity: 0, y: 30 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1, duration: 0.5 }}
                whileHover={{ y: -5, scale: 1.01 }}
              >
                <div className="match-date-section">
                  <div className="match-date">
                    <Calendar size={20} />
                    <span>{new Date(match.date).toLocaleDateString('ko-KR', { month: 'short', day: 'numeric' })}</span>
                  </div>
                  <div className="match-time">
                    <Clock size={18} />
                    <span>{match.time}</span>
                  </div>
                  <div className="match-location">
                    <MapPin size={18} />
                    <span>{match.location}</span>
                  </div>
                </div>

                <div className="match-teams">
                  <div className="team home-team">
                    <div className="team-name">FC쏘아</div>
                    {match.score && <div className="team-score">{match.score.home}</div>}
                  </div>

                  <div className="match-vs">
                    {match.status === 'completed' ? (
                      <div className="result-badge">
                        {getResultIcon(match.result)}
                      </div>
                    ) : (
                      <div className="vs-badge">VS</div>
                    )}
                  </div>

                  <div className="team away-team">
                    {match.score && <div className="team-score">{match.score.away}</div>}
                    <div className="team-name">{match.opponent}</div>
                  </div>
                </div>

                <div className="match-actions">
                  <span className={`status-badge ${match.status}`}>
                    {match.status === 'upcoming' ? '예정' : '종료'}
                  </span>
                  <div className="action-buttons">
                    {match.status === 'upcoming' && (
                      <button className="icon-btn complete" onClick={() => openCompleteModal(match)} title="경기 완료">
                        <CheckCircle size={16} />
                      </button>
                    )}
                    <button className="icon-btn edit" onClick={() => openEditModal(match)} title="수정">
                      <Edit2 size={16} />
                    </button>
                    <button className="icon-btn delete" onClick={() => handleDelete(match.id)} title="삭제">
                      <Trash2 size={16} />
                    </button>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        )}
      </section>

      {/* 경기 추가/수정 모달 */}
      <AnimatePresence>
        {showModal && (
          <motion.div
            className="modal-overlay"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={closeModal}
          >
            <motion.div
              className="modal-content"
              initial={{ scale: 0.8, y: 50 }}
              animate={{ scale: 1, y: 0 }}
              exit={{ scale: 0.8, y: 50 }}
              onClick={e => e.stopPropagation()}
            >
              <div className="modal-header">
                <h2>{editingMatch ? '경기 수정' : '새 경기 추가'}</h2>
                <button className="modal-close" onClick={closeModal}>
                  <X size={24} />
                </button>
              </div>

              <form className="match-form" onSubmit={handleSubmit}>
                <div className="form-row">
                  <div className="form-group">
                    <label>상대팀</label>
                    <input
                      type="text"
                      value={formData.opponent}
                      onChange={e => setFormData({ ...formData, opponent: e.target.value })}
                      placeholder="상대팀 이름"
                      required
                    />
                  </div>
                  <div className="form-group">
                    <label>장소</label>
                    <input
                      type="text"
                      value={formData.location}
                      onChange={e => setFormData({ ...formData, location: e.target.value })}
                      placeholder="경기 장소"
                      required
                    />
                  </div>
                </div>

                <div className="form-row">
                  <div className="form-group">
                    <label>날짜</label>
                    <input
                      type="date"
                      value={formData.match_date}
                      onChange={e => setFormData({ ...formData, match_date: e.target.value })}
                      required
                    />
                  </div>
                  <div className="form-group">
                    <label>시간</label>
                    <input
                      type="time"
                      value={formData.match_time}
                      onChange={e => setFormData({ ...formData, match_time: e.target.value })}
                      required
                    />
                  </div>
                </div>

                <div className="form-row">
                  <div className="form-group">
                    <label>홈/원정</label>
                    <select
                      value={formData.home_away}
                      onChange={e => setFormData({ ...formData, home_away: e.target.value })}
                    >
                      <option value="home">홈</option>
                      <option value="away">원정</option>
                    </select>
                  </div>
                </div>

                <div className="form-actions">
                  <button type="button" className="btn-cancel" onClick={closeModal}>
                    취소
                  </button>
                  <button type="submit" className="btn-submit">
                    <Save size={18} />
                    {editingMatch ? '수정' : '추가'}
                  </button>
                </div>
              </form>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* 경기 완료 모달 */}
      <AnimatePresence>
        {showCompleteModal && completingMatch && (
          <motion.div
            className="modal-overlay"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={closeCompleteModal}
          >
            <motion.div
              className="modal-content modal-large"
              initial={{ scale: 0.8, y: 50 }}
              animate={{ scale: 1, y: 0 }}
              exit={{ scale: 0.8, y: 50 }}
              onClick={e => e.stopPropagation()}
            >
              <div className="modal-header">
                <h2>경기 완료 - vs {completingMatch.opponent}</h2>
                <button className="modal-close" onClick={closeCompleteModal}>
                  <X size={24} />
                </button>
              </div>

              <form className="match-form" onSubmit={handleCompleteSubmit}>
                <div className="form-section">
                  <h3>스코어</h3>
                  <div className="score-input-row">
                    <div className="score-team">
                      <span>FC쏘아</span>
                      <input
                        type="number"
                        min="0"
                        value={completeFormData.fc_ssoa_score}
                        onChange={e => setCompleteFormData({ ...completeFormData, fc_ssoa_score: parseInt(e.target.value) || 0 })}
                        className="score-input"
                      />
                    </div>
                    <span className="score-vs">:</span>
                    <div className="score-team">
                      <input
                        type="number"
                        min="0"
                        value={completeFormData.opponent_score}
                        onChange={e => setCompleteFormData({ ...completeFormData, opponent_score: parseInt(e.target.value) || 0 })}
                        className="score-input"
                      />
                      <span>{completingMatch.opponent}</span>
                    </div>
                  </div>
                </div>

                <div className="form-section">
                  <div className="section-header">
                    <h3>⚽ 골 기록</h3>
                    <button type="button" className="btn-add-entry" onClick={addGoalEntry}>
                      <Plus size={16} /> 추가
                    </button>
                  </div>
                  {completeFormData.goals.map((goal, index) => (
                    <div key={index} className="stat-entry">
                      <select
                        value={goal.player_name}
                        onChange={e => updateGoal(index, 'player_name', e.target.value)}
                        className="player-select"
                      >
                        <option value="">선수 선택</option>
                        {players.map(p => (
                          <option key={p.name} value={p.name}>
                            {p.jersey_number ? `#${p.jersey_number} ` : ''}{p.name}
                          </option>
                        ))}
                      </select>
                      <input
                        type="number"
                        min="1"
                        value={goal.count}
                        onChange={e => updateGoal(index, 'count', e.target.value)}
                        className="count-input"
                      />
                      <button type="button" className="btn-remove" onClick={() => removeGoal(index)}>
                        <X size={16} />
                      </button>
                    </div>
                  ))}
                </div>

                <div className="form-section">
                  <div className="section-header">
                    <h3>🅰️ 어시스트 기록</h3>
                    <button type="button" className="btn-add-entry" onClick={addAssistEntry}>
                      <Plus size={16} /> 추가
                    </button>
                  </div>
                  {completeFormData.assists.map((assist, index) => (
                    <div key={index} className="stat-entry">
                      <select
                        value={assist.player_name}
                        onChange={e => updateAssist(index, 'player_name', e.target.value)}
                        className="player-select"
                      >
                        <option value="">선수 선택</option>
                        {players.map(p => (
                          <option key={p.name} value={p.name}>
                            {p.jersey_number ? `#${p.jersey_number} ` : ''}{p.name}
                          </option>
                        ))}
                      </select>
                      <input
                        type="number"
                        min="1"
                        value={assist.count}
                        onChange={e => updateAssist(index, 'count', e.target.value)}
                        className="count-input"
                      />
                      <button type="button" className="btn-remove" onClick={() => removeAssist(index)}>
                        <X size={16} />
                      </button>
                    </div>
                  ))}
                </div>

                <div className="form-actions">
                  <button type="button" className="btn-cancel" onClick={closeCompleteModal}>
                    취소
                  </button>
                  <button type="submit" className="btn-submit btn-complete">
                    <CheckCircle size={18} />
                    경기 완료
                  </button>
                </div>
              </form>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}

export default Schedule
