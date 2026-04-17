import styles from './Badge.module.scss'

interface BadgeProps {
  className?: string
  children?: React.ReactNode
  onClick?: () => void
}

export const Badge = ({ 
  className, 
  children, 
  onClick, 
}: BadgeProps) => {
  return (
    <div 
      className={`${styles.container} ${className || ''}`}
      onClick={onClick}
    >
      {children || <h1>Badge Component</h1>}
    </div>
  )
}

export default Badge
