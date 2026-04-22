import styles from './Badge.module.scss'

interface BadgeProps {
	className?: string
	children?: React.ReactNode
	onClick?: () => void
	size?: 'small' | 'medium' | 'large'
	type?: 'main' | 'second'
	price?: 'none' | 'up' | 'down'
}

export const Badge = ({
	className,
	children,
	onClick,
	size = 'medium',
	type = 'second',
	price = 'none',
}: BadgeProps) => {
	return (
		<div
			className={`${styles.badge} ${styles[size]} ${styles[type]} ${styles[price]} ${className || ''}`}
			onClick={onClick}
		>
			{price == 'down' ? (
				<img src='/down.svg' alt='Опускается' />
			) : price == 'up' ? (
				<img src='/up.svg' alt='Поднимается' />
			) : (
				''
			)}
			{children}
		</div>
	)
}

export default Badge
