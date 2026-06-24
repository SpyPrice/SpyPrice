import { useTable } from './Table'
import styles from './TableRow.module.scss'

interface TableRowProps {
	className?: string
	children?: React.ReactNode
	onClick?: () => void
	hoverable?: boolean
	selected?: boolean
}

export const TableRow = ({
	className,
	children,
	onClick,
	hoverable = true,
	selected = false,
}: TableRowProps) => {
	const { variant } = useTable()

	return (
		<tr
			className={`
        ${styles.row}
        ${hoverable ? styles.hoverable : ''}
        ${selected ? styles.selected : ''}
        ${variant === 'striped' ? styles.striped : ''}
        ${className || ''}
      `}
			onClick={onClick}
			style={{ cursor: onClick ? 'pointer' : 'default' }}
		>
			{children}
		</tr>
	)
}

export default TableRow
