import Header from '@/Components/Widgets/Header'
import { Outlet } from 'react-router-dom'

export const HeaderLayout = () => {
	return (
		<>
			<Header />
			<Outlet />
		</>
	)
}

export default HeaderLayout
