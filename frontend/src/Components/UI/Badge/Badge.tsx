import styles from './Badge.module.scss'

interface BadgeProps {
	className?: string
	children?: React.ReactNode
	onClick?: () => void
	size?: 'small' | 'medium' | 'large'
}

export const Badge = ({
	className,
	children,
	onClick,
	size = 'medium',
}: BadgeProps) => {
	return (
		<div
			className={`${styles.badge} ${styles[size]} ${className || ''}`}
			onClick={onClick}
		>
			{children}
		</div>
	)
}

export default Badge
