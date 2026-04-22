import { useAuth } from '@/Contexts/AuthContext'
import { Navigate } from 'react-router-dom'

interface PublicRouteProps {
	children: React.ReactNode
}

export const PublicRoute = ({ children }: PublicRouteProps) => {
	const { isAuthenticated, isLoading } = useAuth()

	if (isLoading) {
		return <div>Loading...</div>
	}

	if (isAuthenticated) {
		return <Navigate to='/dashboard' replace />
	}

	return <>{children}</>
}

export default PublicRoute
