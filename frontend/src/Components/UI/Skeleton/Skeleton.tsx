import styles from './Skeleton.module.scss'

interface SkeletonProps {
	className?: string
	children?: React.ReactNode
	onClick?: () => void
}

export const Skeleton = ({ className, children, onClick }: SkeletonProps) => {
	return (
		<div className={`${styles.container} ${className || ''}`} onClick={onClick}>
			{children || <h1>Skeleton Component</h1>}
		</div>
	)
}

export default Skeleton
