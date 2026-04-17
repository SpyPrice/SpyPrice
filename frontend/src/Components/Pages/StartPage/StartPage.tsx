import Button from '@/Components/UI/Button'
import Footer from '@/Components/Widgets/Footer'
import styles from './StartPage.module.scss'

export const StartPage = () => {
	return (
		<>
			<section className={styles.container}>
				<h1>
					Отслеживайте цены. <br />
					Экономьте деньги.
				</h1>
				<h2>
					Добавляйте товары из любимых интернет-магазинов, отслеживайте историю
					цен и покупайте в самый выгодный момент.
				</h2>
				<div className={styles.buttons}>
					<Button>Начать бесплатно</Button>
					<Button>Уже есть аккаунт</Button>
				</div>
			</section>
			<Footer />
		</>
	)
}

export default StartPage
