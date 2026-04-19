import Button from '@/Components/UI/Button'
import Input from '@/Components/UI/Input'
import { useAuth } from '@/Contexts/AuthContext'
import { useTitle } from '@/Hooks'
import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { toast } from 'react-toastify'
import styles from './RegisterPage.module.scss'

export const RegisterPage = () => {
	useTitle('Регистрация')
	const { register } = useAuth()
	const navigate = useNavigate()

	const [inputsData, setInputsData] = useState({
		name: '',
		email: '',
		password: '',
	})
	const [isLoading, setIsLoading] = useState(false)

	const handleSubmit = async (e: React.SubmitEvent<HTMLFormElement>) => {
		e.preventDefault()

		if (!inputsData.email || !inputsData.password || !inputsData.name) {
			toast('Пожалуйста, заполните все поля', { type: 'error' })
			return
		}

		if (inputsData.password.length < 8) {
			toast('Пароль ддолжен быть больше 8 символов', { type: 'error' })
			return
		}

		setIsLoading(true)
		try {
			await register({
				email: inputsData.email,
				password: inputsData.password,
				name: inputsData.name,
			})
			navigate('/dashboard')
		} finally {
			setIsLoading(false)
		}
	}

	return (
		<div className={styles.container}>
			<h2>SpyPrice</h2>
			<form onSubmit={e => handleSubmit(e)} className={styles.block}>
				<p className={styles.register_p}>Создание аккаунта </p>
				<p className={styles.register_p_description}>
					Начните отслеживать цены бесплатно
				</p>
				<div className={styles.input_group}>
					<label htmlFor='name'>Имя</label>
					<Input
						id='name'
						type='text'
						placeholder='Михаил'
						onChange={el =>
							setInputsData({ ...inputsData, name: el.currentTarget.value })
						}
					/>
				</div>
				<div className={styles.input_group}>
					<label htmlFor='email'>Email</label>
					<Input
						id='email'
						type='email'
						placeholder='your@email.ru'
						onChange={el =>
							setInputsData({ ...inputsData, email: el.currentTarget.value })
						}
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
					/>
				</div>
				<Button formType='submit' fullWidth disabled={isLoading}>
					{isLoading ? 'Создание аккаунта...' : 'Создать аккаунт'}
				</Button>

				<p className={styles.have_account}>
					Уже есть аккаунт? <Link to={'/login'}>Войти</Link>
				</p>
			</form>
			<Link to={'/'}>
				<Button type='dark-no-back'>← Вернуться на главную</Button>
			</Link>
		</div>
	)
}

export default RegisterPage
