import styles from './Select.module.scss'

interface SelectProps {
  className?: string
  children?: React.ReactNode
  onClick?: () => void
}

export const Select = ({ 
  className, 
  children, 
  onClick, 
}: SelectProps) => {
  return (
    <div 
      className={`${styles.container} ${className || ''}`}
      onClick={onClick}
    >
      {children || <h1>Select Component</h1>}
    </div>
  )
}

export default Select
