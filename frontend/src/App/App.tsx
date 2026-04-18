import HeaderLayout from '@/Components/Layouts/HeaderLayout'
import LoginPage from '@/Components/Pages/LoginPage'
import RegisterPage from '@/Components/Pages/RegisterPage'
import StartPage from '@/Components/Pages/StartPage'
import '@Styles/global.scss'
import { BrowserRouter, Route, Routes } from 'react-router-dom'
import { ToastContainer } from 'react-toastify'
import NotFoundPage from '../Components/Pages/NotFoundPage'

function App() {
	return (
		<>
			<BrowserRouter>
				<Routes>
					<Route path='/' element={<HeaderLayout />}>
						<Route index element={<StartPage />} />
						<Route path='/dashboard' element={<NotFoundPage />} />
						<Route path='/profile' element={<NotFoundPage />} />
						<Route path='/tracking/:id' element={<NotFoundPage />} />
					</Route>
					<Route path='/login' element={<LoginPage />} />
					<Route path='/register' element={<RegisterPage />} />
					<Route path='*' element={<NotFoundPage />} />
				</Routes>
			</BrowserRouter>
			<ToastContainer position='bottom-right' autoClose={3000} />
		</>
	)
}

export default App
