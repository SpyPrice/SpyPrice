import styles from './Filter.module.scss'

interface FilterProps {
  className?: string
  children?: React.ReactNode
  onClick?: () => void
}

export const Filter = ({ 
  className, 
  children, 
  onClick, 
}: FilterProps) => {
  return (
    <div 
      className={`${styles.container} ${className || ''}`}
      onClick={onClick}
    >
      {children || <h1>Filter Component</h1>}
    </div>
  )
}

export default Filter
