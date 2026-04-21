import { Link, useLocation } from 'react-router-dom'
import styles from './Header.module.scss'

export const Header = () => {
	const location = useLocation()

	return (
		<header className={styles.header}>
			<div className={styles.container}>
				<div className={styles.left}>
					<div className={styles.logo}>
						<img src='/logo.svg' alt='Логотип' />
						<p>SpyPrice</p>
					</div>
					<nav className={styles.nav}>
						<ul>
							<li>
								<Link
									className={`${styles.navLink} ${location.pathname === '/dashboard' ? styles.active : ''}`}
									to={'/dashboard'}
								>
									<img src='/dashboard.svg' alt='Товары' />
									Товары
								</Link>
							</li>
							<li>
								<Link
									className={`${styles.navLink} ${location.pathname === '/shops' ? styles.active : ''}`}
									to={'/shops'}
								>
									<img src='/shop.svg' alt='Магазин' />
									Магазины
								</Link>
							</li>
							<li>
								<Link
									className={`${styles.navLink} ${location.pathname === '/profile' ? styles.active : ''}`}
									to={'/profile'}
								>
									<img src='/profile.svg' alt='Профиль' />
									Профиль
								</Link>
							</li>
						</ul>
					</nav>
				</div>
				<div className={styles.right}>
					{/* <div className='theme'>
					<Button>
						<img src='./dark.svg' />
					</Button>
				</div> */}
				</div>
			</div>
		</header>
	)
}

export default Header
