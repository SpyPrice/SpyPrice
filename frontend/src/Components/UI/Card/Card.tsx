import styles from './Card.module.scss'

interface CardProps {
	className?: string
	children: React.ReactNode
}

export const Card = ({ className, children }: CardProps) => {
	return <div className={`${styles.card} ${className || ''}`}>{children}</div>
}

export default Card
