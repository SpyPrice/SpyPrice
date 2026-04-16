import styles from './StartPage.module.scss'

interface StartPageProps {
  className?: string
  children?: React.ReactNode
  onClick?: () => void
}

export const StartPage = ({ 
  className, 
  children, 
  onClick, 
}: StartPageProps) => {
  return (
    <div 
      className={`${styles.container} ${className || ''}`}
      onClick={onClick}
    >
      {children || <h1>StartPage Component</h1>}
    </div>
  )
}

export default StartPage
