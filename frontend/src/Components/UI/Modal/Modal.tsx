import styles from './Modal.module.scss'

interface ModalProps {
  className?: string
  children?: React.ReactNode
  onClick?: () => void
}

export const Modal = ({ 
  className, 
  children, 
  onClick, 
}: ModalProps) => {
  return (
    <div 
      className={`${styles.container} ${className || ''}`}
      onClick={onClick}
    >
      {children || <h1>Modal Component</h1>}
    </div>
  )
}

export default Modal
