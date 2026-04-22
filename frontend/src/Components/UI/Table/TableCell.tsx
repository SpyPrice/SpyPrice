import styles from './TableCell.module.scss'

interface TableCellProps {
	className?: string
	children?: React.ReactNode
	align?: 'left' | 'center' | 'right'
	colSpan?: number
	isHeader?: boolean
}

export const TableCell = ({
	className,
	children,
	align = 'left',
	colSpan,
	isHeader = false,
}: TableCellProps) => {
	const Component = isHeader ? 'th' : 'td'

	return (
		<Component
			className={`
        ${styles.cell}
        ${styles[align]}
        ${isHeader ? styles.headerCell : ''}
        ${className || ''}
      `}
			colSpan={colSpan}
		>
			{children}
		</Component>
	)
}

export default TableCell
