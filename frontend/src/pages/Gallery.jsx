import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { X, Camera, Play, Youtube } from 'lucide-react'
import axios from 'axios'
import './Gallery.css'

// YouTube API 설정
const YOUTUBE_API_KEY = 'AIzaSyAuK1ffSw8RQB1bwU9K6unuipQAmAcGAAo'
const CHANNEL_HANDLE = '@FC쏘아'

function Gallery() {
  const [videos, setVideos] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [selectedVideo, setSelectedVideo] = useState(null)

  useEffect(() => {
    fetchYouTubeVideos()
  }, [])

  const fetchYouTubeVideos = async () => {
    try {
      // 1. 채널 핸들로 채널 ID 가져오기
      const channelResponse = await axios.get(
        `https://www.googleapis.com/youtube/v3/search?part=snippet&q=${encodeURIComponent(CHANNEL_HANDLE)}&type=channel&key=${YOUTUBE_API_KEY}`
      )

      if (channelResponse.data.items && channelResponse.data.items.length > 0) {
        const channelId = channelResponse.data.items[0].snippet.channelId

        // 2. 채널의 최신 영상 목록 가져오기
        const videosResponse = await axios.get(
          `https://www.googleapis.com/youtube/v3/search?part=snippet&channelId=${channelId}&maxResults=20&order=date&type=video&key=${YOUTUBE_API_KEY}`
        )

        const videoList = videosResponse.data.items.map(item => ({
          id: item.id.videoId,
          title: item.snippet.title,
          thumbnail: item.snippet.thumbnails.high?.url || item.snippet.thumbnails.medium?.url,
          date: item.snippet.publishedAt,
          description: item.snippet.description
        }))

        setVideos(videoList)
      }
      setLoading(false)
    } catch (err) {
      console.error('YouTube API Error:', err)
      setError('영상을 불러오는데 실패했습니다')
      setLoading(false)
    }
  }

  const openVideo = (video) => {
    setSelectedVideo(video)
  }

  const closeVideo = () => {
    setSelectedVideo(null)
  }

  return (
    <div className="gallery-page">
      <section className="gallery-hero">
        <motion.div
          className="gallery-hero-content"
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
        >
          <h1 className="gallery-hero-title">
            경기 <span className="gradient-text">영상</span>
          </h1>
          <p className="gallery-hero-subtitle">
            FC쏘아의 경기 하이라이트와 기록 영상
          </p>
          <a
            href="https://www.youtube.com/@FC쏘아"
            target="_blank"
            rel="noopener noreferrer"
            className="youtube-channel-btn"
          >
            <Youtube size={20} />
            YouTube 채널 방문
          </a>
        </motion.div>
      </section>

      <section className="gallery-content">
        {loading ? (
          <div className="loading-container">
            <div className="loading-spinner" />
            <p>영상을 불러오는 중...</p>
          </div>
        ) : error ? (
          <div className="error-container">
            <p>{error}</p>
          </div>
        ) : (
          <motion.div className="video-grid" layout>
            <AnimatePresence>
              {videos.map((video, index) => (
                <motion.div
                  key={video.id}
                  className="video-item"
                  layout
                  initial={{ opacity: 0, scale: 0.8 }}
                  animate={{ opacity: 1, scale: 1 }}
                  exit={{ opacity: 0, scale: 0.8 }}
                  transition={{ duration: 0.4, delay: index * 0.05 }}
                  whileHover={{ y: -10 }}
                  onClick={() => openVideo(video)}
                >
                  <div className="video-thumbnail-wrapper">
                    <img
                      src={video.thumbnail}
                      alt={video.title}
                      className="video-thumbnail"
                    />
                    <div className="video-play-overlay">
                      <Play className="play-icon" size={48} />
                    </div>
                  </div>
                  <div className="video-info">
                    <h3 className="video-title">{video.title}</h3>
                    <p className="video-date">
                      {new Date(video.date).toLocaleDateString('ko-KR', {
                        year: 'numeric',
                        month: 'long',
                        day: 'numeric'
                      })}
                    </p>
                  </div>
                </motion.div>
              ))}
            </AnimatePresence>
          </motion.div>
        )}
      </section>

      {/* 영상 플레이어 모달 */}
      <AnimatePresence>
        {selectedVideo && (
          <motion.div
            className="video-modal-overlay"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={closeVideo}
          >
            <motion.div
              className="video-modal-content"
              initial={{ scale: 0.8, y: 50 }}
              animate={{ scale: 1, y: 0 }}
              exit={{ scale: 0.8, y: 50 }}
              onClick={(e) => e.stopPropagation()}
            >
              <button className="video-modal-close" onClick={closeVideo}>
                <X size={24} />
              </button>
              <div className="video-player-wrapper">
                <iframe
                  src={`https://www.youtube.com/embed/${selectedVideo.id}?autoplay=1`}
                  title={selectedVideo.title}
                  frameBorder="0"
                  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                  allowFullScreen
                  className="video-player"
                />
              </div>
              <div className="video-modal-info">
                <h2 className="video-modal-title">{selectedVideo.title}</h2>
                <p className="video-modal-date">
                  {new Date(selectedVideo.date).toLocaleDateString('ko-KR', {
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric'
                  })}
                </p>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}

export default Gallery
