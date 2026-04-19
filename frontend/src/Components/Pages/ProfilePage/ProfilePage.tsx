import Button from '@/Components/UI/Button'
import Card from '@/Components/UI/Card'
import styles from './ProfilePage.module.scss'

export const ProfilePage = () => {
	return (
		<div className={styles.container}>
			<h2>Профиль</h2>
			<p>Управление вашим аккаунтом</p>
			<Card className={styles.info_card}>
				<h3>Информация об аккаунте</h3>
				<p>Данные вашего профиля</p>
				<div className={styles.info_group}>
					<Card className={styles.info_item}>
						<img src='/email.svg' alt='Почта' />
						<div className={styles.info_text}>
							<p className={styles.info_label}>Email</p>
							<p className={styles.info_value}>example@mail.ru</p>
						</div>
					</Card>
					<Card className={styles.info_item}>
						<img src='/calendar.svg' alt='Календарь' />
						<div className={styles.info_text}>
							<p className={styles.info_label}>Дата регистрации</p>
							<p className={styles.info_value}>19 апреля 2026 г.</p>
						</div>
					</Card>
				</div>
			</Card>

			<Card className={styles.actions_card}>
				<h3>Действия</h3>
				<Button type='danger'>
					<img src='/delete.svg' alt='Удалить' />
					<p>Выйти из аккаунта</p>
				</Button>
			</Card>
		</div>
	)
}

export default ProfilePage
