# FaceScan Access - Setup Guide

## Prerequisites

### Software Requirements
- **Windows 10/11**
- **Docker Desktop for Windows** ([Download](https://www.docker.com/products/docker-desktop))
- **Node.js 18+** ([Download](https://nodejs.org/))
- **Git** ([Download](https://git-scm.com/))

### Hardware Requirements
- 8GB RAM minimum
- 6-12 core CPU
- IP cameras with RTSP support OR USB webcam
- Gate/boom barrier with control relay (optional for testing)

---

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/Drake0306/facescan-Access.git
cd facescan-Access
```

### 2. Setup Environment Variables

```bash
# Copy the example environment file
copy .env.example .env

# Edit .env with your configuration (optional for initial testing)
notepad .env
```

**Important Settings:**
- Default credentials will be created automatically
- Camera settings can use webcam by default (index 0 and 1)
- Gate controller is in MOCK mode by default

### 3. Start Backend Services (Docker)

Open PowerShell or Command Prompt in the project directory:

```bash
# Start all Docker containers
docker-compose up -d

# Check if containers are running
docker-compose ps
```

**Services Started:**
- PostgreSQL Database (port 5432)
- pgAdmin (port 5050) - Database management UI
- Backend API (port 8000)
- Face Recognition Service (port 8001)
- Gate Controller (port 8002)

### 4. Initialize Database

```bash
# Run database initialization script
docker-compose exec backend python -m app.db.init_db
```

**Default Users Created:**
- **Admin**: username=`admin`, password=`admin123`
- **Guard**: username=`guard`, password=`guard123`

### 5. Setup Electron Desktop App

```bash
cd electron-app

# Install dependencies
npm install

# Create environment file
copy .env.example .env

# Start development server
npm run dev
```

The Electron app will automatically open.

---

## Testing the System

### 1. Login to the Application

- Open the Electron app
- Login with: `admin` / `admin123`

### 2. Access Backend Services

**API Documentation (Swagger):**
```
http://localhost:8000/docs
```

**Database Management (pgAdmin):**
```
http://localhost:5050
Email: admin@facescan.local
Password: admin_password_here
```

**Face Recognition Service:**
```
http://localhost:8001/docs
```

**Gate Controller:**
```
http://localhost:8002/docs
```

### 3. Test Face Detection

1. Navigate to Dashboard in the Electron app
2. Go to Visitors page
3. Click "Add Visitor"
4. Upload a photo with a clear face
5. System will detect and encode the face

---

## Camera Configuration

### Using Webcam (Default)

Already configured in `.env`:
```env
ENTRY_CAMERA_TYPE=webcam
ENTRY_CAMERA_INDEX=0
EXIT_CAMERA_TYPE=webcam
EXIT_CAMERA_INDEX=1
```

### Using IP Cameras (RTSP)

Edit `.env` file:
```env
ENTRY_CAMERA_TYPE=rtsp
ENTRY_CAMERA_RTSP=rtsp://username:password@192.168.1.100:554/stream
EXIT_CAMERA_TYPE=rtsp
EXIT_CAMERA_RTSP=rtsp://username:password@192.168.1.101:554/stream
```

**Restart services after changing camera settings:**
```bash
docker-compose restart face-service
```

---

## Gate Controller Setup

### Mock Mode (Testing - Default)

No hardware needed. Gates will be simulated.

```env
GATE_CONTROLLER_TYPE=mock
```

### HTTP Relay Device

For network-based relay devices:

```env
GATE_CONTROLLER_TYPE=http
GATE_CONTROLLER_HOST=192.168.1.50
GATE_CONTROLLER_PORT=80
```

### Serial/USB Relay

For USB or serial relay modules:

```env
GATE_CONTROLLER_TYPE=serial
GATE_CONTROLLER_SERIAL_PORT=COM3
GATE_CONTROLLER_BAUD_RATE=9600
```

**Note:** Restart gate-controller service after changes:
```bash
docker-compose restart gate-controller
```

---

## Development Workflow

### Starting Development

```bash
# Terminal 1 - Start backend services
docker-compose up

# Terminal 2 - Start Electron app
cd electron-app
npm run dev
```

### Viewing Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f face-service
```

### Stopping Services

```bash
# Stop all containers
docker-compose down

# Stop and remove volumes (WARNING: deletes data)
docker-compose down -v
```

---

## Building for Production

### Build Electron App

```bash
cd electron-app
npm run build
npm run build:electron
```

Executable will be in `electron-app/release/`

### Deploy Backend

For production deployment, update `.env` with:
- Strong SECRET_KEY
- Secure database passwords
- Production CORS origins
- Disable DEBUG mode

---

## Troubleshooting

### Docker containers won't start

```bash
# Check Docker is running
docker --version

# Check ports are not in use
netstat -ano | findstr :5432
netstat -ano | findstr :8000

# Rebuild containers
docker-compose down
docker-compose build --no-cache
docker-compose up
```

### Face recognition not working

```bash
# Check camera connection
docker-compose exec face-service python -c "import cv2; print(cv2.VideoCapture(0).isOpened())"

# View face service logs
docker-compose logs -f face-service
```

### Database connection errors

```bash
# Check PostgreSQL is running
docker-compose ps postgres

# Reinitialize database
docker-compose exec backend python app/db/init_db.py
```

### Electron app won't connect to backend

1. Verify backend is running: `http://localhost:8000/health`
2. Check `.env` in electron-app:
   ```env
   VITE_API_URL=http://localhost:8000/api/v1
   ```
3. Clear browser cache (Ctrl+Shift+R in Electron)

---

## Next Steps

### Phase 1 Complete - You Have:
- ✅ Working backend API with database
- ✅ Face detection and recognition service
- ✅ Gate controller service
- ✅ Electron desktop app with UI
- ✅ Multi-user authentication
- ✅ Visitor management foundation

### Phase 2 - To Implement:
1. **Real-time face recognition from camera streams**
2. **Visitor registration with face enrollment**
3. **Automatic gate triggering**
4. **Entry/exit logging**
5. **Live camera feeds in UI**
6. **WebSocket real-time updates**

### Customization

Modify configurations in:
- Backend API: `backend/app/core/config.py`
- Face Service: `face-service/app/core/config.py`
- Gate Controller: `gate-controller/app/core/config.py`
- Electron App: `electron-app/src/renderer/lib/api.ts`

---

## Support

- Report issues: [GitHub Issues](https://github.com/Drake0306/facescan-Access/issues)
- Check logs for errors
- Review API documentation at `/docs` endpoints

## Security Notes

**IMPORTANT for Production:**
1. Change all default passwords
2. Use strong JWT secret key
3. Enable HTTPS
4. Restrict CORS origins
5. Use environment-specific `.env` files
6. Never commit `.env` files to git
