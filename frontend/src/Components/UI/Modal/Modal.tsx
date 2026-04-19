import { useEffect, useRef } from 'react'
import styles from './Modal.module.scss'

interface ModalProps {
	isOpen: boolean
	onClose: () => void
	title?: string
	children: React.ReactNode
	size?: 'small' | 'medium' | 'large' | 'full'
	closeOnOverlayClick?: boolean
	closeOnEsc?: boolean
	showCloseButton?: boolean
	footer?: React.ReactNode
}

export const Modal = ({
	isOpen,
	onClose,
	title,
	children,
	size = 'medium',
	closeOnOverlayClick = true,
	closeOnEsc = true,
	showCloseButton = true,
	footer,
}: ModalProps) => {
	const modalRef = useRef<HTMLDivElement>(null)

	useEffect(() => {
		const handleEsc = (event: KeyboardEvent) => {
			if (closeOnEsc && event.key === 'Escape' && isOpen) {
				onClose()
			}
		}

		if (isOpen) {
			document.addEventListener('keydown', handleEsc)
			document.body.style.overflow = 'hidden'
		}

		return () => {
			document.removeEventListener('keydown', handleEsc)
			document.body.style.overflow = 'unset'
		}
	}, [isOpen, onClose, closeOnEsc])

	const handleOverlayClick = (e: React.MouseEvent) => {
		if (closeOnOverlayClick && e.target === e.currentTarget) {
			onClose()
		}
	}

	if (!isOpen) return null

	return (
		<div className={styles.overlay} onClick={handleOverlayClick}>
			<div ref={modalRef} className={`${styles.modal} ${styles[size]}`}>
				{(title || showCloseButton) && (
					<div className={styles.header}>
						{title && <h2 className={styles.title}>{title}</h2>}
						{showCloseButton && (
							<button
								className={styles.closeButton}
								onClick={onClose}
								aria-label='Закрыть'
							>
								×
							</button>
						)}
					</div>
				)}

				<div className={styles.content}>{children}</div>

				{footer && <div className={styles.footer}>{footer}</div>}
			</div>
		</div>
	)
}

export default Modal
