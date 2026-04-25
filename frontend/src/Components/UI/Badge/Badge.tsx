import DownIcon from '@/Assets/down.svg?react'
import UpIcon from '@/Assets/up.svg?react'
import styles from './Badge.module.scss'

interface BadgeProps {
	className?: string
	children?: React.ReactNode
	onClick?: () => void
	size?: 'small' | 'medium' | 'large'
	type?: 'main' | 'second'
	price?: 'none' | 'up' | 'down' | 'equals'
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
			{price == 'down' ? <DownIcon /> : price == 'up' ? <UpIcon /> : ''}
			{children}
		</div>
	)
}

export default Badge
