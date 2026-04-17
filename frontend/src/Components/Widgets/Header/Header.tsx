import Button from '@/Components/UI/Button'
import styles from './Header.module.scss'

export const Header = () => {
	return (
		<header className={`${styles.container}`}>
			<div className='logo'></div>
			<div className='right'>
				<div className='theme'>
					<Button>
						<img src='./dark.svg' />
					</Button>
				</div>
				<div className='auth_buttons'>
					<Button>Войти</Button>
					<Button>Регистрация</Button>
				</div>
			</div>
		</header>
	)
}

export default Header
