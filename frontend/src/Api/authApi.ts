import api from './axios'

export interface UserCreate {
	email: string
	name: string
	password: string
}

export interface UserRead {
	id: number
	email: string
	name: string
	is_active: boolean
	created_at: string
}

export interface Token {
	access_token: string
	token_type: string
}

export interface TokenWithUser extends Token {
	user: UserRead
}

export const authApi = {
	register: (data: UserCreate) => api.post<TokenWithUser>('/register', data),

	login: async (username: string, password: string) => {
		const formData = new URLSearchParams()
		formData.append('username', username)
		formData.append('password', password)

		return api.post<Token>('/login', formData, {
			headers: {
				'Content-Type': 'application/x-www-form-urlencoded',
			},
		})
	},

	getMe: () => api.get<UserRead>('/me'),
}
