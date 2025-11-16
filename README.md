# FaceScan Access - Face-Based Gate Pass System

A comprehensive visitor management and gate access control system using facial recognition technology.

## Features

- **Real-time Face Recognition**: Detect and recognize faces from IP cameras or webcams
- **Automated Gate Control**: Automatically open gates for recognized visitors
- **Visitor Management**: Register new visitors with facial enrollment
- **Entry/Exit Tracking**: Complete audit trail of all gate activities
- **Multi-User Support**: Role-based access control for guards and administrators
- **Day/Night Operation**: Optimized for both daylight and IR camera feeds
- **Offline Capable**: Core functionality works without internet connectivity
- **Data Retention**: Configurable auto-deletion of logs and photos

## Tech Stack

- **Frontend**: Electron + React + TypeScript + shadcn/ui + Tailwind CSS
- **Backend API**: Python + FastAPI + SQLAlchemy
- **Face Recognition**: OpenCV + face_recognition/DeepFace
- **Database**: PostgreSQL with pgvector extension
- **Containerization**: Docker + Docker Compose

## System Requirements

- Windows 10/11
- 8GB RAM minimum
- 6-12 core CPU
- Docker Desktop for Windows
- IP cameras with RTSP support or USB webcam

## Project Structure

```
facescan-Access/
├── docker-compose.yml          # Container orchestration
├── .env.example                # Environment variables template
├── electron-app/               # Desktop application
│   ├── src/
│   │   ├── main/              # Electron main process
│   │   ├── renderer/          # React UI
│   │   └── preload/           # Preload scripts
│   ├── package.json
│   └── tsconfig.json
├── backend/                    # FastAPI backend service
│   ├── app/
│   │   ├── api/               # API routes
│   │   ├── models/            # Database models
│   │   ├── schemas/           # Pydantic schemas
│   │   ├── services/          # Business logic
│   │   └── core/              # Configuration
│   ├── Dockerfile
│   └── requirements.txt
├── face-service/               # Face recognition service
│   ├── app/
│   │   ├── detection/         # Face detection
│   │   ├── recognition/       # Face matching
│   │   ├── camera/            # Camera handling
│   │   └── preprocessing/     # Image enhancement
│   ├── Dockerfile
│   └── requirements.txt
└── gate-controller/            # Gate hardware control
    ├── app/
    ├── Dockerfile
    └── requirements.txt
```

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/Drake0306/facescan-Access.git
cd facescan-Access
```

### 2. Setup Environment Variables

```bash
cp .env.example .env
# Edit .env with your configuration
```

### 3. Start Backend Services

```bash
docker-compose up -d
```

### 4. Install and Run Desktop App

```bash
cd electron-app
npm install
npm run dev
```

## Development

### Backend Development

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend Development

```bash
cd electron-app
npm run dev
```

### Database Access

- **pgAdmin**: http://localhost:5050
- **Credentials**: See docker-compose.yml

## Configuration

### Camera Setup

Edit `.env` file:
```
ENTRY_CAMERA_RTSP=rtsp://camera-ip:554/stream
EXIT_CAMERA_RTSP=rtsp://camera-ip:554/stream
# Or use webcam index
ENTRY_CAMERA_INDEX=0
```

### Gate Controller

Configure hardware connection in `.env`:
```
GATE_CONTROLLER_TYPE=http  # Options: http, serial, gpio, mock
GATE_CONTROLLER_URL=http://relay-device-ip/api
```

## API Documentation

Once the backend is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## License

MIT License - See LICENSE file for details

## Support

For issues and feature requests, please use GitHub Issues.
