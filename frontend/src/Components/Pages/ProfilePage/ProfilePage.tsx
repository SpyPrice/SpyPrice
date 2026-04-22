import Button from '@/Components/UI/Button'
import Card from '@/Components/UI/Card'
import { useAuth } from '@/Contexts/AuthContext'
import { useTitle } from '@/Hooks'
import { useNavigate } from 'react-router-dom'
import styles from './ProfilePage.module.scss'

export const ProfilePage = () => {
	useTitle('Профиль')
	const { user, logout } = useAuth()
	const navigate = useNavigate()

	const formatDate = (dateString?: string) => {
		if (!dateString) return 'Не указана'
		const date = new Date(dateString)
		return date.toLocaleDateString('ru-RU', {
			year: 'numeric',
			month: 'long',
			day: 'numeric',
		})
	}

	return (
		<div className={styles.container}>
			<h2>Профиль</h2>
			<p>Управление вашим аккаунтом</p>
			<Card className={styles.info_card}>
				<h3>Информация об аккаунте</h3>
				<p>Данные вашего профиля</p>
				<div className={styles.info_group}>
					<Card className={styles.info_item}>
						<img src='/profile.svg' alt='Пользователь' />
						<div className={styles.info_text}>
							<p className={styles.info_label}>Имя пользователя</p>
							<p className={styles.info_value}>{user?.name}</p>
						</div>
					</Card>
					<Card className={styles.info_item}>
						<img src='/email.svg' alt='Почта' />
						<div className={styles.info_text}>
							<p className={styles.info_label}>Email</p>
							<p className={styles.info_value}>{user?.email}</p>
						</div>
					</Card>
					<Card className={styles.info_item}>
						<img src='/calendar.svg' alt='Календарь' />
						<div className={styles.info_text}>
							<p className={styles.info_label}>Дата регистрации</p>
							<p className={styles.info_value}>
								{formatDate(user?.created_at)}
							</p>
						</div>
					</Card>
				</div>
			</Card>

			<Card className={styles.actions_card}>
				<h3>Действия</h3>
				<Button
					type='warning'
					onClick={() => {
						logout()
						navigate('/')
					}}
				>
					<img src='/logout.svg' alt='Выход' />
					<p>Выйти из аккаунта</p>
				</Button>
			</Card>
		</div>
	)
}

export default ProfilePage
