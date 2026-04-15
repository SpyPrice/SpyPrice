import styles from './Button.module.scss'

interface ButtonProps {
  className?: string
  children?: React.ReactNode
  onClick?: () => void
  disabled?: boolean
}

export const Button = ({ 
  className, 
  children, 
  onClick, 
  disabled = false 
}: ButtonProps) => {
  return (
    <div 
      className={`${styles.container} ${className || ''}`}
      onClick={!disabled ? onClick : undefined}
      aria-disabled={disabled}
    >
      {children || <h1>Button Component</h1>}
    </div>
  )
}

export default Button
