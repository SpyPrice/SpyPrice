import styles from './Card.module.scss'

interface CardProps {
	className?: string
	children: React.ReactNode
	onClick?: () => void
}

export const Card = ({ className, children, onClick }: CardProps) => {
	return (
		<div
			className={`${styles.card} ${className || ''} ${onClick && styles.click}`}
			onClick={onClick}
		>
			{children}
		</div>
	)
}

export default Card
