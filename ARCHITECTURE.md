# FaceScan Access - System Architecture

## Overview

FaceScan Access is a face-based gate pass and visitor tracking system designed for automated access control using facial recognition technology.

## System Components

### 1. Electron Desktop Application (Frontend)

**Location:** `electron-app/`

**Tech Stack:**
- Electron 28
- React 18
- TypeScript
- shadcn/ui (Radix UI + Tailwind CSS)
- React Router
- TanStack Query
- Zustand (State Management)
- Socket.IO Client

**Key Features:**
- Multi-user authentication (Admin, Guard)
- Real-time dashboard with camera feeds
- Visitor management interface
- Live notifications via WebSocket
- Responsive UI with shadcn/ui components

**Structure:**
```
electron-app/
├── src/
│   ├── main/           # Electron main process
│   ├── preload/        # IPC bridge
│   └── renderer/       # React application
│       ├── components/ # UI components
│       ├── pages/      # Application pages
│       ├── lib/        # Utilities, API, WebSocket
│       └── stores/     # State management
```

---

### 2. Backend API Service

**Location:** `backend/`

**Tech Stack:**
- Python 3.11
- FastAPI
- SQLAlchemy ORM
- PostgreSQL
- JWT Authentication
- Socket.IO (WebSocket)

**Responsibilities:**
- User authentication and authorization
- Visitor CRUD operations
- Visit/access log management
- Gate control coordination
- Real-time event broadcasting
- API for all client applications

**Database Schema:**
- `users` - System users (guards, admins)
- `visitors` - Registered visitors
- `faces` - Face embeddings linked to visitors
- `visits` - Entry/exit records
- `gate_events` - Gate action audit trail

**API Endpoints:**
- `/api/v1/auth/*` - Authentication
- `/api/v1/visitors/*` - Visitor management
- `/api/v1/visits/*` - Visit logs
- `/api/v1/gate/*` - Gate control
- `/api/v1/reports/*` - Analytics

---

### 3. Face Recognition Service

**Location:** `face-service/`

**Tech Stack:**
- Python 3.11
- FastAPI
- OpenCV
- face_recognition library
- NumPy

**Responsibilities:**
- Face detection in images/video frames
- Face encoding generation
- Face comparison and matching
- Camera stream management (RTSP/Webcam)
- Image preprocessing (day/night enhancement)
- Real-time face recognition pipeline

**Features:**
- Multiple detection models (HOG, CNN)
- Adaptive brightness enhancement for night mode
- Configurable recognition threshold
- Support for RTSP IP cameras and USB webcams
- Multi-camera management (entry/exit)

**API Endpoints:**
- `/api/v1/detection/detect` - Detect faces in image
- `/api/v1/detection/encode` - Generate face encoding
- `/api/v1/recognition/compare` - Compare two faces
- `/api/v1/recognition/identify` - Identify against database

---

### 4. Gate Controller Service

**Location:** `gate-controller/`

**Tech Stack:**
- Python 3.11
- FastAPI
- PySerial (for serial relays)
- Requests (for HTTP relays)

**Responsibilities:**
- Physical gate control (open/close)
- Auto-close timer
- Status monitoring
- Support for multiple relay types

**Supported Hardware:**
- **Mock Mode** - Testing without hardware
- **HTTP Relay** - Network-based relay devices
- **Serial Relay** - USB/RS-232 relay modules
- **GPIO** - Raspberry Pi GPIO (planned)

**API Endpoints:**
- `/api/v1/gate/open` - Open gate
- `/api/v1/gate/close` - Close gate
- `/api/v1/gate/status` - Get gate status

---

### 5. PostgreSQL Database

**Container:** `postgres:15-alpine`

**Features:**
- UUID extension enabled
- Stores all application data
- Optimized for relationship queries
- Full ACID compliance

**Access:**
- Direct: `localhost:5432`
- pgAdmin: `http://localhost:5050`

---

### 6. pgAdmin (Database Management)

**Container:** `dpage/pgadmin4`

**Purpose:**
- Visual database administration
- Query execution
- Schema inspection
- Data export/import

**Access:** `http://localhost:5050`

---

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    Windows Desktop (PC)                      │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │         Electron App (Guard/Admin Interface)           │ │
│  │  - React UI with shadcn/ui                             │ │
│  │  - Real-time WebSocket updates                         │ │
│  │  - Visitor management                                  │ │
│  └────────────────────────────────────────────────────────┘ │
│                            │ HTTP/WebSocket                  │
│                            ▼                                 │
│  ┌────────────────────────────────────────────────────────┐ │
│  │                Docker Containers                        │ │
│  │                                                         │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │ │
│  │  │   Backend    │  │     Face     │  │     Gate     │ │ │
│  │  │   API        │  │  Recognition │  │  Controller  │ │ │
│  │  │   :8000      │  │   Service    │  │   Service    │ │ │
│  │  │              │  │   :8001      │  │   :8002      │ │ │
│  │  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘ │ │
│  │         │                 │                 │          │ │
│  │         └────────┬────────┴─────────────────┘          │ │
│  │                  ▼                                      │ │
│  │         ┌─────────────────┐                            │ │
│  │         │   PostgreSQL    │                            │ │
│  │         │     :5432       │                            │ │
│  │         └─────────────────┘                            │ │
│  │                                                         │ │
│  └─────────────────────────────────────────────────────────┘ │
│                            │                                 │
│              ┌─────────────┴─────────────┐                  │
│              ▼                           ▼                   │
│    ┌──────────────────┐        ┌──────────────────┐        │
│    │   IP Cameras     │        │  Gate/Relay      │        │
│    │   (RTSP/USB)     │        │  Hardware        │        │
│    └──────────────────┘        └──────────────────┘        │
└─────────────────────────────────────────────────────────────┘
```

---

## Data Flow

### 1. Face Recognition Flow

```
Camera Feed → Face Service (detect) → Face Service (encode)
                                           │
                                           ▼
                                    Backend (match with DB)
                                           │
                                           ▼
                            ┌──────────────┴──────────────┐
                            ▼                             ▼
                     Known Visitor                 Unknown Visitor
                            │                             │
                            ▼                             ▼
                    Gate Opens (auto)              UI Alert (manual)
                            │                             │
                            ▼                             ▼
                    Visit Log Created              Guard Registers
```

### 2. Visitor Registration Flow

```
Guard → Upload Photo → Face Service (detect & encode)
                              │
                              ▼
                       Embedding Generated
                              │
                              ▼
                Backend (save visitor + embedding)
                              │
                              ▼
                    Database (visitors + faces)
```

### 3. Entry/Exit Flow

```
Person at Gate → Camera Capture → Face Recognition
                                          │
                                          ▼
                                   Match Found?
                                    │         │
                              Yes ──┘         └── No
                                │                  │
                                ▼                  ▼
                         Check Status        Notify Guard
                        (inside/outside)           │
                                │                  └─> Manual Decision
                                ▼
                         Open Gate
                                │
                                ▼
                      Create Visit Record
                                │
                                ▼
                     WebSocket → UI Update
```

---

## Communication Protocols

### HTTP REST API
- Electron App ↔ Backend API
- Backend ↔ Face Service
- Backend ↔ Gate Controller

### WebSocket (Socket.IO)
- Backend → Electron App (real-time events)
- Events: face_detected, gate_opened, visitor_registered

### RTSP
- IP Cameras → Face Service (video stream)

### Serial/HTTP
- Gate Controller → Physical Relay Device

---

## Security Architecture

### Authentication
- JWT-based authentication
- Role-based access control (Admin, Guard)
- Token expiration and refresh
- Secure password hashing (bcrypt)

### API Security
- CORS configuration
- Request validation
- SQL injection prevention (ORM)
- Input sanitization

### Data Security
- Sensitive data encryption at rest
- Secure face embedding storage
- Environment variable configuration
- No hardcoded credentials

---

## Scalability Considerations

### Horizontal Scaling
- Backend API: Multiple instances behind load balancer
- Face Service: Distributed processing queue
- Database: Read replicas for reporting

### Performance Optimization
- Face embedding caching
- Database indexing on lookup fields
- WebSocket connection pooling
- Image preprocessing pipeline

### Storage Optimization
- Face embeddings: Binary storage
- Photos: Configurable retention
- Logs: Auto-deletion after N days

---

## Deployment Architecture

### Development
- Docker Compose on single machine
- Hot reload for all services
- Mock hardware for testing

### Production
- Kubernetes cluster (optional)
- Separate database server
- Load balancer for API
- CDN for static assets
- Backup and monitoring

---

## Technology Choices Rationale

| Component | Technology | Reason |
|-----------|-----------|--------|
| Desktop App | Electron | Cross-platform, native feel, hardware access |
| Frontend | React + TypeScript | Type safety, component reusability |
| UI Library | shadcn/ui | Modern, accessible, customizable |
| Backend | FastAPI | Fast, async, auto-documentation |
| ORM | SQLAlchemy | Mature, feature-rich, PostgreSQL support |
| Database | PostgreSQL | Robust, ACID, great for relationships |
| Face Recognition | face_recognition | Easy to use, accurate, battle-tested |
| Computer Vision | OpenCV | Industry standard, comprehensive |
| Containerization | Docker | Consistent environments, easy deployment |

---

## Future Enhancements

### Phase 2 (Planned)
- Real-time video streaming in UI
- Multiple gate support
- Advanced reporting and analytics
- Email/SMS notifications
- Blacklist management
- Time-based access rules

### Phase 3 (Future)
- Mobile app for guards
- Cloud backup and sync
- AI-powered anomaly detection
- Integration with HR systems
- Visitor self-registration kiosk
- Multi-language support
- Advanced anti-spoofing

---

## Development Guidelines

### Code Organization
- Feature-based folder structure
- Separation of concerns
- Single responsibility principle
- DRY (Don't Repeat Yourself)

### Naming Conventions
- Python: snake_case
- TypeScript: camelCase
- Components: PascalCase
- Constants: UPPER_SNAKE_CASE

### API Design
- RESTful principles
- Consistent response format
- Proper HTTP status codes
- Comprehensive error messages

### Testing (To Be Implemented)
- Unit tests for services
- Integration tests for APIs
- E2E tests for critical flows
- Mock hardware for testing

---

## Monitoring and Logging

### Logging Levels
- DEBUG: Development details
- INFO: Normal operations
- WARNING: Potential issues
- ERROR: Errors requiring attention
- CRITICAL: System failures

### Metrics to Monitor
- API response times
- Face recognition accuracy
- Gate operation success rate
- Database query performance
- WebSocket connection health

---

## Troubleshooting Guide

See [SETUP.md](./SETUP.md) for detailed troubleshooting steps.

### Common Issues
1. Camera not detected → Check device permissions
2. Face not recognized → Adjust threshold
3. Gate not opening → Check relay connection
4. Database errors → Verify connection string
5. WebSocket disconnects → Check network stability

---

## Contributing

1. Follow the project structure
2. Use TypeScript/Python type hints
3. Write descriptive commit messages
4. Update documentation
5. Test before committing

---

## License

MIT License - See [LICENSE](./LICENSE) for details
