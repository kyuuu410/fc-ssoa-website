import { motion } from 'framer-motion'
import '../pages/Team.css'

function TeamMemberList({ members, position, positionColor }) {
  return (
    <div className="members-grid">
      {members.map((member, index) => (
        <motion.div
          key={member.id}
          className="member-card"
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ delay: index * 0.1, duration: 0.5 }}
          whileHover={{ y: -10, scale: 1.02 }}
        >
          <div className="member-number" style={{ borderColor: positionColor }}>
            {member.number}
          </div>
          <div className="member-info">
            <h3 className="member-name">{member.name}</h3>
            <p className="member-role">{member.role}</p>
            <p className="member-joined">Since {member.joinedYear}</p>
          </div>
          <div className="member-stats">
            {Object.entries(member.stats).map(([key, value]) => (
              <div key={key} className="stat-item">
                <span className="stat-value">{value}</span>
                <span className="stat-key">{key}</span>
              </div>
            ))}
          </div>
          <div className="member-gradient" style={{ background: `linear-gradient(135deg, ${positionColor}22 0%, transparent 100%)` }} />
        </motion.div>
      ))}
    </div>
  )
}

export default TeamMemberList
