import axios from 'axios'
import { useAuthStore } from '@/stores/authStore'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
const FACE_SERVICE_URL = import.meta.env.VITE_FACE_SERVICE_URL || 'http://localhost:8001'

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const faceServiceApi = axios.create({
  baseURL: FACE_SERVICE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = useAuthStore.getState().token
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      useAuthStore.getState().logout()
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// API endpoints
export const authAPI = {
  login: (username: string, password: string) =>
    api.post('/auth/login', { username, password }),
  logout: () => api.post('/auth/logout'),
  me: () => api.get('/auth/me'),
}

export const visitorsAPI = {
  getAll: (params?: { search?: string; skip?: number; limit?: number }) =>
    api.get('/visitors', { params }),
  getById: (id: string) => api.get(`/visitors/${id}`),
  create: (data: any) => api.post('/visitors', data),
  update: (id: string, data: any) => api.put(`/visitors/${id}`, data),
  delete: (id: string) => api.delete(`/visitors/${id}`),
}

export const visitsAPI = {
  getAll: (params?: { skip?: number; limit?: number; visitor_id?: string }) =>
    api.get('/visits', { params }),
  getActive: () => api.get('/visits/active'),
  create: (data: any) => api.post('/visits', data),
  update: (id: string, data: any) => api.put(`/visits/${id}`, data),
}

export const gateAPI = {
  open: (gateId: string) => api.post(`/gate/${gateId}/open`),
  close: (gateId: string) => api.post(`/gate/${gateId}/close`),
  status: (gateId: string) => api.get(`/gate/${gateId}/status`),
}

export const reportsAPI = {
  getDailySummary: (date: string) => api.get('/reports/daily', { params: { date } }),
  getVisitorFrequency: (startDate: string, endDate: string) =>
    api.get('/reports/frequency', { params: { start_date: startDate, end_date: endDate } }),
  export: (params: any) => api.get('/reports/export', { params, responseType: 'blob' }),
}

export const cameraAPI = {
  listAvailable: () => faceServiceApi.get('/api/v1/detection/cameras/list'),
  configure: (entryIndex?: number, exitIndex?: number) =>
    faceServiceApi.post('/api/v1/detection/cameras/configure', null, {
      params: {
        entry_index: entryIndex,
        exit_index: exitIndex,
      },
    }),
  getStatus: () => faceServiceApi.get('/api/v1/detection/camera/status'),
  frameUrl: (which: 'entry' | 'exit') =>
    `${FACE_SERVICE_URL}/api/v1/detection/cameras/frame?camera=${which}`,
  reset: (entryIndex?: number, exitIndex?: number, restartServices?: boolean) =>
    faceServiceApi.post('/api/v1/detection/cameras/reset', null, {
      params: {
        entry_index: entryIndex,
        exit_index: exitIndex,
        restart_services: restartServices,
      },
      timeout: 15000,
    }),
}
