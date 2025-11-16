import { io, Socket } from 'socket.io-client'
import { useAuthStore } from '@/stores/authStore'

const WS_URL = import.meta.env.VITE_WS_URL || 'http://localhost:8000'

class WebSocketService {
  private socket: Socket | null = null

  connect() {
    const token = useAuthStore.getState().token

    this.socket = io(WS_URL, {
      auth: {
        token,
      },
      transports: ['websocket'],
    })

    this.socket.on('connect', () => {
      console.log('WebSocket connected')
    })

    this.socket.on('disconnect', () => {
      console.log('WebSocket disconnected')
    })

    this.socket.on('error', (error) => {
      console.error('WebSocket error:', error)
    })

    return this.socket
  }

  disconnect() {
    if (this.socket) {
      this.socket.disconnect()
      this.socket = null
    }
  }

  on(event: string, callback: (...args: any[]) => void) {
    if (this.socket) {
      this.socket.on(event, callback)
    }
  }

  off(event: string, callback?: (...args: any[]) => void) {
    if (this.socket) {
      this.socket.off(event, callback)
    }
  }

  emit(event: string, data?: any) {
    if (this.socket) {
      this.socket.emit(event, data)
    }
  }

  getSocket() {
    return this.socket
  }
}

export const wsService = new WebSocketService()
