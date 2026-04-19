import HeaderLayout from '@/Components/Layouts/HeaderLayout'
import PublicLayout from '@/Components/Layouts/PublicLayout'
import DashboardPage from '@/Components/Pages/DashboardPage'
import LoginPage from '@/Components/Pages/LoginPage'
import ProfilePage from '@/Components/Pages/ProfilePage'
import RegisterPage from '@/Components/Pages/RegisterPage'
import StartPage from '@/Components/Pages/StartPage'
import { AuthProvider } from '@/Contexts/AuthContext'
import '@Styles/global.scss'
import { BrowserRouter, Route, Routes } from 'react-router-dom'
import { ToastContainer } from 'react-toastify'
import NotFoundPage from '../Components/Pages/NotFoundPage'

function App() {
	return (
		<>
			<AuthProvider>
				<BrowserRouter>
					<Routes>
						<Route element={<HeaderLayout />}>
							<Route path='/dashboard' element={<DashboardPage />} />
							<Route path='/profile' element={<ProfilePage />} />
							<Route path='/tracking/:id' element={<NotFoundPage />} />
						</Route>
						<Route element={<PublicLayout />}>
							<Route path='/' element={<StartPage />} />
							<Route path='/login' element={<LoginPage />} />
							<Route path='/register' element={<RegisterPage />} />
						</Route>
						<Route path='*' element={<NotFoundPage />} />
					</Routes>
				</BrowserRouter>
				<ToastContainer position='bottom-right' autoClose={3000} />
			</AuthProvider>
		</>
	)
}

export default App
