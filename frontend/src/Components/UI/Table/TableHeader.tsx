import styles from './TableHeader.module.scss'

interface TableHeaderProps {
	className?: string
	children?: React.ReactNode
	sticky?: boolean
}

export const TableHeader = ({
	className,
	children,
	sticky = false,
}: TableHeaderProps) => {
	return (
		<thead className={sticky ? styles.sticky : ''}>
			<tr className={`${styles.header} ${className || ''}`}>{children}</tr>
		</thead>
	)
}

export default TableHeader
