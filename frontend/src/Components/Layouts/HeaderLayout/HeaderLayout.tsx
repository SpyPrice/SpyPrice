import Header from '@/Components/Widgets/Header'
import { Outlet } from 'react-router-dom'
import ProtectedRoute from '../ProtectedRoute'

export const HeaderLayout = () => {
	return (
		<>
			<ProtectedRoute>
				<Header />
				<Outlet />
			</ProtectedRoute>
		</>
	)
}

export default HeaderLayout
