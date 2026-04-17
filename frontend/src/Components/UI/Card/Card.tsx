import styles from './Card.module.scss'

interface CardProps {
  className?: string
  children?: React.ReactNode
  onClick?: () => void
}

export const Card = ({ 
  className, 
  children, 
  onClick, 
}: CardProps) => {
  return (
    <div 
      className={`${styles.container} ${className || ''}`}
      onClick={onClick}
    >
      {children || <h1>Card Component</h1>}
    </div>
  )
}

export default Card
