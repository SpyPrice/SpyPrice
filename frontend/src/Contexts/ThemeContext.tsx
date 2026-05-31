import React, {
	createContext,
	useContext,
	useLayoutEffect,
	useState,
	type ReactNode,
} from 'react'

const ThemeContext = createContext<ThemeContextType | undefined>(undefined)

export type Theme = 'light' | 'dark'

export interface ThemeContextType {
	theme: Theme
	toggleTheme: () => void
}

interface ThemeProviderProps {
	children: ReactNode
}

const getInitialTheme = (): Theme => {
	const savedTheme = localStorage.getItem('theme') as Theme
	if (savedTheme) return savedTheme

	const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
	return prefersDark ? 'dark' : 'light'
}

const applyThemeClass = (theme: Theme) => {
	const root = document.documentElement

	if (theme === 'dark') {
		root.classList.add('dark_theme')
		root.classList.remove('light_theme')
	} else {
		root.classList.add('light_theme')
		root.classList.remove('dark_theme')
	}
}

export const ThemeProvider: React.FC<ThemeProviderProps> = ({ children }) => {
	const [theme, setTheme] = useState<Theme>(() => {
		const initialTheme = getInitialTheme()
		applyThemeClass(initialTheme)
		return initialTheme
	})

	const toggleTheme = () => {
		setTheme(prevTheme => (prevTheme === 'light' ? 'dark' : 'light'))
	}

	useLayoutEffect(() => {
		applyThemeClass(theme)
		localStorage.setItem('theme', theme)
	}, [theme])

	return (
		<ThemeContext.Provider value={{ theme, toggleTheme }}>
			{children}
		</ThemeContext.Provider>
	)
}

export const useTheme = (): ThemeContextType => {
	const context = useContext(ThemeContext)
	if (!context) {
		throw new Error('useTheme must be used within ThemeProvider')
	}
	return context
}
