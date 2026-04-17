import Button from '@/Components/UI/Button'
import Card from '@/Components/UI/Card'
import Footer from '@/Components/Widgets/Footer'
import { Link } from 'react-router-dom'
import styles from './StartPage.module.scss'

export const StartPage = () => {
	return (
		<>
			<section className={styles.main_block}>
				<h1>
					Отслеживайте цены. <br />
					Экономьте деньги.
				</h1>
				<h2>
					Добавляйте товары из любимых интернет-магазинов, отслеживайте историю
					цен и покупайте в самый выгодный момент.
				</h2>
				<div className={styles.buttons}>
					<Link to={'/register'}>
						<Button size='large'>Начать бесплатно</Button>
					</Link>
					<Link to={'/login'}>
						<Button size='large' type='light'>
							Уже есть аккаунт
						</Button>
					</Link>
				</div>
			</section>
			<section className={styles.cards}>
				<Card>
					<div className={`${styles.card_img} ${styles.card_img_blue}`}>
						<img src='/arrow.svg' alt='Стрелка' />
					</div>
					<p className={styles.card_header}>Добавьте ссылку</p>
					<p className={styles.card_content}>
						Просто вставьте URL товара из DNS, Ozon, Wildberries и других
						магазинов
					</p>
				</Card>
				<Card>
					<div className={`${styles.card_img} ${styles.card_img_purple}`}>
						<img src='/chart.svg' alt='График' />
					</div>
					<p className={styles.card_header}>Смотрите графики</p>
					<p className={styles.card_content}>
						Отслеживайте динамику цен за любой период и анализируйте тренды
					</p>
				</Card>
				<Card>
					<div className={`${styles.card_img} ${styles.card_img_green}`}>
						<img src='/bell.svg' alt='Колкольчик' />
					</div>
					<p className={styles.card_header}>Получайте уведомления</p>
					<p className={styles.card_content}>
						Узнавайте первыми о снижении цен на интересующие вас товары
					</p>
				</Card>
			</section>
			<section className={styles.create_account_block}>
				<div className={styles.info_block}>
					<h2>Готовы начать экономить?</h2>
					<h3>
						Присоединяйтесь к тысячам пользователей, которые уже следят за
						ценами
					</h3>
					<Button size='large' type='light'>
						Создать аккаунт
					</Button>
				</div>
			</section>
			<Footer />
		</>
	)
}

export default StartPage
