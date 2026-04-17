import styles from './Input.module.scss'

interface InputProps {
  className?: string
  children?: React.ReactNode
  onClick?: () => void
}

export const Input = ({ 
  className, 
  children, 
  onClick, 
}: InputProps) => {
  return (
    <div 
      className={`${styles.container} ${className || ''}`}
      onClick={onClick}
    >
      {children || <h1>Input Component</h1>}
    </div>
  )
}

export default Input
