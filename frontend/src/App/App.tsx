import '@Styles/global.scss'
import '@Styles/variables.scss'
import { BrowserRouter, Route, Routes } from 'react-router-dom'
import NotFoundPage from '../Components/Page/NotFoundPage'

function App() {
	return (
		<>
			<BrowserRouter>
				<Routes>
					<Route path='/' element={<NotFoundPage />} />
					<Route path='/login' element={<NotFoundPage />} />
					<Route path='/register' element={<NotFoundPage />} />
					<Route path='/profile' element={<NotFoundPage />} />
					<Route path='/tracking/:id' element={<NotFoundPage />} />
					<Route path='*' element={<NotFoundPage />} />
				</Routes>
			</BrowserRouter>
		</>
	)
}

export default App
