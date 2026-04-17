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

	login: (username: string, password: string) =>
		api.post<Token>('/login', { username, password }),

	getMe: () => {
		api.get<UserRead>('/me')
	},
}
