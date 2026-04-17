import Button from '@/Components/UI/Button'
import Input from '@/Components/UI/Input'
import { useState } from 'react'
import { Link } from 'react-router-dom'
import styles from './LoginPage.module.scss'

export const LoginPage = () => {
	const [inputsData, setInputsData] = useState({ email: '', password: '' })

	return (
		<div className={styles.container}>
			<h2>SpyPrice</h2>
			<div className={styles.block}>
				<p>Вход в аккаунт</p>
				<div className={styles.inputgroup}>
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
				<div className={styles.inputgroup}>
					<label htmlFor='password'>Пароль</label>
					<Input
						id='password'
						type='password'
						onChange={el =>
							setInputsData({ ...inputsData, password: el.currentTarget.value })
						}
					/>
				</div>
				<Button fullWidth>Войти</Button>

				<p>
					Нет аккаунта? <Link to={'/register'}>Зарегистрироваться</Link>
				</p>
			</div>
			<Link to={'/'}>
				<Button type='dark-no-back'>← Вернуться на главную</Button>
			</Link>
		</div>
	)
}

export default LoginPage
