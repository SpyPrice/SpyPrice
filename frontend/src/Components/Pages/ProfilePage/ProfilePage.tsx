import CalendarIcon from '@/Assets/calendar.svg?react'
import EmailIcon from '@/Assets/email.svg?react'
import LogoutIcon from '@/Assets/logout.svg?react'
import MoonIcon from '@/Assets/moon.svg?react'
import ProfileIcon from '@/Assets/profile.svg?react'
import SunIcon from '@/Assets/sun.svg?react'
import Button from '@/Components/UI/Button'
import Card from '@/Components/UI/Card'
import { useAuth } from '@/Contexts/AuthContext'
import { useTheme } from '@/Contexts/ThemeContext'
import { useTitle } from '@/Hooks'
import { useNavigate } from 'react-router-dom'
import styles from './ProfilePage.module.scss'

export const ProfilePage = () => {
	useTitle('Профиль')

	const { theme, toggleTheme } = useTheme()
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
						<ProfileIcon />
						<div className={styles.info_text}>
							<p className={styles.info_label}>Имя пользователя</p>
							<p className={styles.info_value}>{user?.name}</p>
						</div>
					</Card>
					<Card className={styles.info_item}>
						<EmailIcon />
						<div className={styles.info_text}>
							<p className={styles.info_label}>Email</p>
							<p className={styles.info_value}>{user?.email}</p>
						</div>
					</Card>
					<Card className={styles.info_item}>
						<CalendarIcon />
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
				<div className={styles.buttons}>
					<Button
						type={`${theme}`}
						onClick={() => {
							toggleTheme()
						}}
					>
						{theme === 'dark' ? <MoonIcon /> : <SunIcon />}
						<p>{theme === 'dark' ? 'Темная' : 'Светлая'} тема</p>
					</Button>
					<Button
						type='warning'
						onClick={() => {
							logout()
							navigate('/')
						}}
					>
						<LogoutIcon />
						<p>Выйти из аккаунта</p>
					</Button>
				</div>
			</Card>
		</div>
	)
}

export default ProfilePage
