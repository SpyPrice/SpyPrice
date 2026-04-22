import { createContext, useContext } from 'react'
import styles from './Table.module.scss'

interface TableContextType {
	variant?: 'default' | 'striped' | 'bordered'
	size?: 'small' | 'medium' | 'large'
}

const TableContext = createContext<TableContextType>({})

export const useTable = () => useContext(TableContext)

interface TableProps {
	className?: string
	children?: React.ReactNode
	variant?: 'default' | 'striped' | 'bordered'
	size?: 'small' | 'medium' | 'large'
	fullWidth?: boolean
}

export const Table = ({
	className,
	children,
	variant = 'default',
	size = 'medium',
	fullWidth = true,
}: TableProps) => {
	return (
		<TableContext.Provider value={{ variant, size }}>
			<div className={styles.tableWrapper}>
				<table
					className={`
            ${styles.table}
            ${styles[variant]}
            ${styles[size]}
            ${fullWidth ? styles.fullWidth : ''}
            ${className || ''}
          `}
				>
					{children}
				</table>
			</div>
		</TableContext.Provider>
	)
}

export default Table
