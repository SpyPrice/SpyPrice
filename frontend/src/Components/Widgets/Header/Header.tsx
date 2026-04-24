import BurgerIcon from '@/Assets/burger.svg?react'
import Button from '@/Components/UI/Button'
import { useEffect, useRef, useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import styles from './Header.module.scss'

export const Header = () => {
	const [isMenuOpen, setIsMenuOpen] = useState(false)
	const location = useLocation()
	const menuRef = useRef<HTMLElement>(null)
	const burgerButtonRef = useRef<HTMLButtonElement>(null)

	// Закрытие меню при клике вне области навигации
	useEffect(() => {
		const handleClickOutside = (event: MouseEvent) => {
			if (
				isMenuOpen &&
				menuRef.current &&
				!menuRef.current.contains(event.target as Node) &&
				burgerButtonRef.current &&
				!burgerButtonRef.current.contains(event.target as Node)
			) {
				setIsMenuOpen(false)
			}
		}

		document.addEventListener('mousedown', handleClickOutside)
		return () => {
			document.removeEventListener('mousedown', handleClickOutside)
		}
	}, [isMenuOpen])

	// Закрытие меню при смене роута
	useEffect(() => {
		setIsMenuOpen(false)
	}, [location])

	// Блокировка скролла при открытом меню
	useEffect(() => {
		if (isMenuOpen) {
			document.body.style.overflow = 'hidden'
		} else {
			document.body.style.overflow = 'unset'
		}
		return () => {
			document.body.style.overflow = 'unset'
		}
	}, [isMenuOpen])

	return (
		<header className={styles.header}>
			<div className={styles.container}>
				<div className={styles.left}>
					<div className={styles.logo}>
						<img src='/logo.svg' alt='Логотип' />
						<p>SpyPrice</p>
					</div>
					<Button
						ref={burgerButtonRef}
						className={styles.burgerButton}
						size='small'
						type='light-no-back'
						onClick={() => {
							setIsMenuOpen(!isMenuOpen)
						}}
					>
						<BurgerIcon />
					</Button>
					<nav
						ref={menuRef}
						className={`${styles.nav} ${isMenuOpen ? styles.open : ''}`}
					>
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
			{isMenuOpen && (
				<div
					className={styles.menuOverlay}
					onClick={() => setIsMenuOpen(false)}
				/>
			)}
		</header>
	)
}

export default Header
