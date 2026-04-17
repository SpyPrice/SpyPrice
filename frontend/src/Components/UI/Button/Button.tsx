import styles from './Button.module.scss'

interface ButtonProps {
	className?: string
	children: React.ReactNode
	type?: 'dark' | 'light' | 'dark-no-back'
	size?: 'small' | 'medium' | 'large'
	fullWidth?: boolean
	onClick?: () => void
	disabled?: boolean
}

export const Button = ({
	className,
	children,
	size = 'medium',
	type = 'dark',
	fullWidth = false,
	onClick,
	disabled = false,
}: ButtonProps) => {
	return (
		<button
			className={`${styles.button} 
        ${styles[type]} 
        ${styles[size]}
        ${fullWidth ? styles.fullWidth : ''}
        ${className || ''}`}
			onClick={!disabled ? onClick : undefined}
			disabled={disabled}
		>
			{children}
		</button>
	)
}

export default Button
