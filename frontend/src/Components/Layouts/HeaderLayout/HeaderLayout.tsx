import styles from './HeaderLayout.module.scss'

interface HeaderLayoutProps {
  className?: string
  children?: React.ReactNode
  onClick?: () => void
  disabled?: boolean
}

export const HeaderLayout = ({ 
  className, 
  children, 
  onClick, 
  disabled = false 
}: HeaderLayoutProps) => {
  return (
    <div 
      className={`${styles.container} ${className || ''}`}
      onClick={!disabled ? onClick : undefined}
      aria-disabled={disabled}
    >
      {children || <h1>HeaderLayout Component</h1>}
    </div>
  )
}

export default HeaderLayout
