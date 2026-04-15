import styles from './Header.module.scss'

interface HeaderProps {
  className?: string
  children?: React.ReactNode
  onClick?: () => void
  disabled?: boolean
}

export const Header = ({ 
  className, 
  children, 
  onClick, 
  disabled = false 
}: HeaderProps) => {
  return (
    <div 
      className={`${styles.container} ${className || ''}`}
      onClick={!disabled ? onClick : undefined}
      aria-disabled={disabled}
    >
      {children || <h1>Header Component</h1>}
    </div>
  )
}

export default Header
