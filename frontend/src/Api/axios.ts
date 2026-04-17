import axios from 'axios'

const api = axios.create({
	baseURL: import.meta.env.VITE_SERVER_URL || 'http://localhost:3000/api',
	timeout: 10000,
	headers: {
		'Content-Type': 'application/json',
	},
})

// Request interceptor
api.interceptors.request.use(
	config => {
		const token = localStorage.getItem('access_token')
		if (token) {
			config.headers.Authorization = `Bearer ${token}`
		}
		return config
	},
	error => {
		return Promise.reject(error)
	},
)

// Response interceptor
api.interceptors.response.use(
	response => response.data,
	error => {
		if (error.response?.status === 401) {
			localStorage.removeItem('access_token')
			window.location.href = '/login'
		}
		return Promise.reject(error)
	},
)

export default api
