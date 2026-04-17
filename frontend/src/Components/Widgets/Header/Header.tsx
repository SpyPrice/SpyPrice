import Button from '@/Components/UI/Button'
import { Link } from 'react-router-dom'
import styles from './Header.module.scss'

export const Header = () => {
	return (
		<header className={styles.header}>
			<div className={styles.logo}>
				<img src='/logo.svg' alt='Логотип' />
				SpyPrice
			</div>
			<div className={styles.right}>
				{/* <div className='theme'>
					<Button>
						<img src='./dark.svg' />
					</Button>
				</div> */}
				<div className={styles.auth_buttons}>
					<Link to={'/login'}>
						<Button type='dark-no-back'>Войти</Button>
					</Link>
					<Link to={'/register'}>
						<Button>Регистрация</Button>
					</Link>
				</div>
			</div>
		</header>
	)
}

export default Header
