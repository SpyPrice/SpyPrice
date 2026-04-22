import { Outlet } from 'react-router-dom'
import PublicRoute from '../PublicRoute'

export const PublicLayout = () => {
	return (
		<>
			<PublicRoute>
				<Outlet />
			</PublicRoute>
		</>
	)
}

export default PublicLayout
