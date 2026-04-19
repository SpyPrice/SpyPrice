import { authApi, type UserCreate, type UserRead } from '@/Api/authApi'
import { createContext, useContext, useEffect, useState } from 'react'
import { toast } from 'react-toastify'

interface AuthContextType {
	user: UserRead | null
	isLoading: boolean
	isAuthenticated: boolean
	login: (email: string, password: string) => Promise<void>
	register: (data: UserCreate) => Promise<void>
	logout: () => void
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export const AuthProvider = ({ children }: { children: any }) => {
	const [user, setUser] = useState<UserRead | null>(null)
	const [isLoading, setIsLoading] = useState(true)

	useEffect(() => {
		checkAuth()
	}, [])

	const checkAuth = async () => {
		const token = localStorage.getItem('access_token')
		if (token) {
			try {
				const userData = await authApi.getMe()
				setUser(userData!)
			} catch (error) {
				localStorage.removeItem('access_token')
				console.error('Auth check failed:', error)
			}
		}
		setIsLoading(false)
	}

	const login = async (email: string, password: string) => {
		try {
			const response = await authApi.login(email, password)
			localStorage.setItem('access_token', response.data.access_token)

			const userData = await authApi.getMe()
			setUser(userData!)

			toast.success('Успешный вход!')
		} catch (error) {
			toast.error('Ошибка входа!')
			throw error
		}
	}

	const register = async (data: UserCreate) => {
		try {
			const response = await authApi.register(data)
			localStorage.setItem('access_token', response.data.access_token)
			setUser(response.data.user)
			toast.success('Регистрация успешна')
		} catch (error) {
			toast.error('Ошибка регистрации!')
			throw error
		}
	}

	const logout = () => {
		localStorage.removeItem('access_token')
		setUser(null)
		toast.info('Вы вышли из системы!')
	}

	return (
		<AuthContext.Provider
			value={{
				user,
				isLoading,
				isAuthenticated: !!user,
				login,
				register,
				logout,
			}}
		>
			{children}
		</AuthContext.Provider>
	)
}

export const useAuth = () => {
	const context = useContext(AuthContext)

	if (!context) {
		throw new Error('useAuth must be used within AuthProvider')
	}
	return context
}
