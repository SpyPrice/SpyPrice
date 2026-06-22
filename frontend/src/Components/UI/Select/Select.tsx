import { useEffect, useRef, useState } from 'react'
import styles from './Select.module.scss'

interface Option {
	value: string
	label: string
}

interface CustomSelectProps {
	value: string
	onChange: (value: string) => void
	options: Option[]
	placeholder?: string
}

export const Select = ({
	value,
	onChange,
	options,
	placeholder = 'Выберите',
}: CustomSelectProps) => {
	const [isOpen, setIsOpen] = useState(false)
	const selectRef = useRef<HTMLDivElement>(null)

	const selectedOption = options.find(opt => opt.value === value)

	useEffect(() => {
		const handleClickOutside = (event: MouseEvent) => {
			if (
				selectRef.current &&
				!selectRef.current.contains(event.target as Node)
			) {
				setIsOpen(false)
			}
		}
		document.addEventListener('mousedown', handleClickOutside)
		return () => document.removeEventListener('mousedown', handleClickOutside)
	}, [])

	const handleSelect = (optionValue: string) => {
		onChange(optionValue)
		setIsOpen(false)
	}

	return (
		<div ref={selectRef} className={styles.customSelect}>
			<div
				className={`${styles.selectHeader} ${isOpen ? styles.open : ''}`}
				onClick={() => setIsOpen(!isOpen)}
			>
				<span className={styles.selectedValue}>
					{selectedOption?.label || placeholder}
				</span>
				<span
					className={`${styles.arrow} ${isOpen ? styles.arrowUp : styles.arrowDown}`}
				>
					<svg
						width='16'
						height='16'
						viewBox='0 0 16 16'
						fill='none'
						xmlns='http://www.w3.org/2000/svg'
					>
						<path
							d='M4 6L8 10L12 6'
							stroke='currentColor'
							strokeWidth='1.5'
							strokeLinecap='round'
							strokeLinejoin='round'
						/>
					</svg>
				</span>
			</div>

			{isOpen && (
				<ul className={styles.selectDropdown}>
					{options.map(option => (
						<li
							key={option.value}
							className={`${styles.selectOption} ${option.value === value ? styles.selected : ''}`}
							onClick={() => handleSelect(option.value)}
						>
							{option.label}
							{option.value === value && (
								<span className={styles.checkmark}>
									<svg
										width='16'
										height='16'
										viewBox='0 0 16 16'
										fill='none'
										xmlns='http://www.w3.org/2000/svg'
									>
										<path
											d='M3 8L6.5 12L13 4'
											stroke='currentColor'
											strokeWidth='1.5'
											strokeLinecap='round'
											strokeLinejoin='round'
										/>
									</svg>
								</span>
							)}
						</li>
					))}
				</ul>
			)}
		</div>
	)
}

export default Select
