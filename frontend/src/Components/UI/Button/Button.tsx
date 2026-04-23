import styles from './Button.module.scss'

interface ButtonProps {
	className?: string
	children: React.ReactNode
	type?:
		| 'dark'
		| 'light'
		| 'dark-no-back'
		| 'light-no-back'
		| 'danger'
		| 'warning'
		| 'none'
	size?: 'small' | 'medium' | 'large'
	fullWidth?: boolean
	onClick?: () => void
	disabled?: boolean
	formType?: 'button' | 'submit' | 'reset'
}

export const Button = ({
	className,
	children,
	size = 'medium',
	type = 'dark',
	fullWidth = false,
	onClick,
	disabled = false,
	formType = 'button',
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
			type={formType}
		>
			{children}
		</button>
	)
}

export default Button
