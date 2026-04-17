import HeaderLayout from '@/Components/Layouts/HeaderLayout'
import StartPage from '@/Components/Pages/StartPage'
import '@Styles/global.scss'
import '@Styles/variables.scss'
import { BrowserRouter, Route, Routes } from 'react-router-dom'
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
					<Route path='/login' element={<NotFoundPage />} />
					<Route path='/register' element={<NotFoundPage />} />
					<Route path='*' element={<NotFoundPage />} />
				</Routes>
			</BrowserRouter>
		</>
	)
}

export default App
