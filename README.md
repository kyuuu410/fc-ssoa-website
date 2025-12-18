# FC SSOA Website

**FC SSOA**는 제가 속한 조기축구팀을 위해 만든 웹사이트입니다.
그동안 꾸준히 기록해온 팀 데이터를 반영하여 팀원들이 정보를 쉽게 확인할 수 있도록 제작하였습니다.
또한, 직접 웹사이트를 구축하고 서버를 배포해보며 개발 역량을 키우기 위한 학습 목적으로 진행된 프로젝트입니다.

## 🚀 배포 주소 (Live Demo)

웹사이트는 현재 아래 주소에서 확인하실 수 있습니다.

- **URL**: [https://fc-ssoa-frontend.onrender.com/](https://fc-ssoa-frontend.onrender.com/)
- **Hosting**: Render.com (Free Tier)

---

## 🛠 기술 스택 (Tech Stack)

이 프로젝트는 다음과 같은 기술들을 사용하여 개발되었습니다.

### Frontend
- **Core**: React, Vite
- **Routing**: React Router DOM
- **Styling & Animations**: Framer Motion (애니메이션), Lucide React (아이콘)
- **HTTP Client**: Axios

### Backend
- **Framework**: FastAPI
- **Server**: Uvicorn
- **Validation**: Pydantic

---

## ✨ 주요 기능 (Features)

- **팀 데이터 시각화**: 축적된 조기축구팀 데이터를 웹사이트에 반영
- **반응형 웹 디자인**: 데스크탑 및 모바일 환경 지원
- **부드러운 애니메이션**: Framer Motion을 활용한 인터랙티브한 UI
- **RESTful API**: FastAPI 기반의 고성능 백엔드 API

---

## 📂 프로젝트 구조 (Project Structure)

```
fc-ssoa-website/
├── frontend/          # React 프론트엔드 애플리케이션
│   ├── src/           # 소스 코드
│   ├── public/        # 정적 파일
│   └── ...
├── backend/           # Python FastAPI 백엔드 애플리케이션
│   ├── routers/       # API 라우터
│   ├── main.py        # 애플리케이션 진입점
│   └── ...
└── README.md          # 프로젝트 문서
```

---

## 🏁 시작하기 (Getting Started)

로컬 환경에서 프로젝트를 실행하는 방법입니다.

### 1. Frontend 실행

```bash
# frontend 디렉토리로 이동
cd frontend

# 의존성 패키지 설치
npm install

# 개발 서버 실행
npm run dev
```
브라우저에서 `http://localhost:5173`으로 접속하여 확인합니다.

### 2. Backend 실행

```bash
# backend 디렉토리로 이동
cd backend

# (선택사항) 가상환경 생성 및 활성화
python -m venv venv
# Windows
.\venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

# 의존성 패키지 설치
pip install -r requirements.txt

# 서버 실행
python main.py
```
백엔드 서버는 기본적으로 `http://localhost:8000`에서 실행됩니다. API 문서는 `http://localhost:8000/docs`에서 확인할 수 있습니다.
