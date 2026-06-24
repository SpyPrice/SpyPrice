import styles from './TableHeader.module.scss'

interface TableBodyProps {
	className?: string
	children?: React.ReactNode
}

export const TableBody = ({ className, children }: TableBodyProps) => {
	return (
		<tbody className={`${styles.body} ${className || ''}`}>{children}</tbody>
	)
}

export default TableBody
