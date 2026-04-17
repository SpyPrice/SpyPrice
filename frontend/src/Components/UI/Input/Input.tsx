import styles from './Input.module.scss'

interface InputProps {
	className?: string
	id?: string
	type?: 'text' | 'email' | 'password' | ''
	value?: string | number
	defaultValue?: string | number
	placeholder?: string
	onChange?: React.ChangeEventHandler<HTMLInputElement, HTMLInputElement>
}

export const Input = ({
	className,
	id,
	type = 'text',
	value,
	defaultValue,
	placeholder,
	onChange,
	...props
}: InputProps) => {
	return (
		<input
			className={`${styles.input} ${className || ''}`}
			id={id}
			type={type}
			value={value}
			defaultValue={defaultValue}
			placeholder={placeholder}
			onChange={onChange}
			{...props}
		/>
	)
}

export default Input
