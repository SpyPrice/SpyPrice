import Header from '@/Components/Widgets/Header'
import { Outlet } from 'react-router-dom'

export const HeaderLayout = () => {
	return (
		<>
			{/* <ProtectedRoute> */}
			<Header />
			<Outlet />
			{/* </ProtectedRoute> */}
		</>
	)
}

export default HeaderLayout
