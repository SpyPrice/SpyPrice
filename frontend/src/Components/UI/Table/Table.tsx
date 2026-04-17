import styles from './Table.module.scss'

interface TableProps {
  className?: string
  children?: React.ReactNode
  onClick?: () => void
}

export const Table = ({ 
  className, 
  children, 
  onClick, 
}: TableProps) => {
  return (
    <div 
      className={`${styles.container} ${className || ''}`}
      onClick={onClick}
    >
      {children || <h1>Table Component</h1>}
    </div>
  )
}

export default Table
