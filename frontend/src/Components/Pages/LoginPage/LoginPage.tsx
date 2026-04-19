import Button from '@/Components/UI/Button'
import Input from '@/Components/UI/Input'
import { useAuth } from '@/Contexts/AuthContext'
import { useTitle } from '@/Hooks'
import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import styles from './LoginPage.module.scss'

export const LoginPage = () => {
	useTitle('Вход в аккаунт')
	const { login } = useAuth()
	const navigate = useNavigate()

	const [inputsData, setInputsData] = useState({ email: '', password: '' })
	const [isLoading, setIsLoading] = useState(false)
	const [errorMessage, setErrorMessage] = useState('')

	const handleSubmit = async (e: React.SubmitEvent<HTMLFormElement>) => {
		e.preventDefault()
		if (!inputsData.email || !inputsData.password) {
			setErrorMessage('Пожалуйста, заполните все поля')
			return
		}

		setIsLoading(true)
		try {
			await login(inputsData.email, inputsData.password)
			navigate('/dashboard')
		} finally {
			setIsLoading(false)
		}
	}

	return (
		<div className={styles.container}>
			<h2>SpyPrice</h2>
			<form onSubmit={e => handleSubmit(e)} className={styles.block}>
				<p className={styles.login_p}>Вход в аккаунт</p>
				<p className={styles.login_p_description}>
					Введите ваш email и пароль для входа
				</p>
				<div className={styles.input_group}>
					<label htmlFor='email'>Email</label>
					<Input
						id='email'
						type='email'
						placeholder='your@email.ru'
						onChange={el =>
							setInputsData({ ...inputsData, email: el.currentTarget.value })
						}
						required
					/>
				</div>
				<div className={styles.input_group}>
					<label htmlFor='password'>Пароль</label>
					<Input
						id='password'
						type='password'
						placeholder='••••••••'
						onChange={el =>
							setInputsData({ ...inputsData, password: el.currentTarget.value })
						}
						required
					/>
				</div>
				<Button formType='submit' fullWidth disabled={isLoading}>
					{isLoading ? 'Вход...' : 'Войти'}
				</Button>

				<p className={styles.no_account}>
					Нет аккаунта? <Link to={'/register'}>Зарегистрироваться</Link>
				</p>
			</form>
			<Link to={'/'}>
				<Button type='dark-no-back'>← Вернуться на главную</Button>
			</Link>
		</div>
	)
}

export default LoginPage
