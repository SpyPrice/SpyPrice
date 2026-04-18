import Button from '@/Components/UI/Button'
import Input from '@/Components/UI/Input'
import { useState } from 'react'
import { Link } from 'react-router-dom'
import styles from './RegisterPage.module.scss'

export const RegisterPage = () => {
	const [inputsData, setInputsData] = useState({
		email: '',
		password: '',
		repeat_password: '',
	})

	return (
		<div className={styles.container}>
			<h2>SpyPrice</h2>
			<div className={styles.block}>
				<p className={styles.register_p}>Создание аккаунта </p>
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
				<div className={styles.input_group}>
					<label htmlFor='repeat_password'>Подтвердите пароль</label>
					<Input
						id='repeat_password'
						type='password'
						placeholder='••••••••'
						onChange={el =>
							setInputsData({
								...inputsData,
								repeat_password: el.currentTarget.value,
							})
						}
					/>
				</div>
				<Button fullWidth>Создать аккаунт</Button>

				<p className={styles.have_account}>
					Уже есть аккаунт? <Link to={'/login'}>Войти</Link>
				</p>
			</div>
			<Link to={'/'}>
				<Button type='dark-no-back'>← Вернуться на главную</Button>
			</Link>
		</div>
	)
}

export default RegisterPage
