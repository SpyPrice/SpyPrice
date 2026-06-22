import BurgerIcon from '@/Assets/burger.svg?react'
import DashboardIcon from '@/Assets/dashboard.svg?react'
import MoonIcon from '@/Assets/moon.svg?react'
import ProfileIcon from '@/Assets/profile.svg?react'
import ShopIcon from '@/Assets/shop.svg?react'
import SunIcon from '@/Assets/sun.svg?react'
import Button from '@/Components/UI/Button'
import { useTheme } from '@/Contexts/ThemeContext'
import { useEffect, useRef, useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import styles from './Header.module.scss'

export const Header = () => {
	const [isMenuOpen, setIsMenuOpen] = useState(false)
	const location = useLocation()
	const menuRef = useRef<HTMLElement>(null)
	const burgerButtonRef = useRef<HTMLButtonElement>(null)
	const { theme, toggleTheme } = useTheme()

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

	useEffect(() => {
		setIsMenuOpen(false)
	}, [location])

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
					<Link className={styles.logo} to={'/dashboard'}>
						<img src='/logo.svg' alt='Логотип' />
						<p>SpyPrice</p>
					</Link>
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
									<DashboardIcon />
									Товары
								</Link>
							</li>
							<li>
								<Link
									className={`${styles.navLink} ${location.pathname === '/shops' ? styles.active : ''}`}
									to={'/shops'}
								>
									<ShopIcon />
									Магазины
								</Link>
							</li>
							<li>
								<Link
									className={`${styles.navLink} ${location.pathname === '/profile' ? styles.active : ''}`}
									to={'/profile'}
								>
									<ProfileIcon />
									Профиль
								</Link>
							</li>
						</ul>
					</nav>
				</div>
				<div className={styles.right}>
					<div className='theme'>
						<Button
							type='dark-no-back'
							onClick={() => {
								toggleTheme()
							}}
						>
							{theme === 'dark' ? <MoonIcon /> : <SunIcon />}
						</Button>
					</div>
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
