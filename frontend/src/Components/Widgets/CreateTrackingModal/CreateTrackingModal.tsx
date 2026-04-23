import { cardsApi } from '@/Api/trackingApi'
import DeleteIcon from '@/Assets/delete.svg?react'
import Badge from '@/Components/UI/Badge'
import Button from '@/Components/UI/Button'
import Input from '@/Components/UI/Input'
import Modal from '@/Components/UI/Modal'
import { useRef, useState, type Dispatch, type SetStateAction } from 'react'
import { toast } from 'react-toastify'
import styles from './CreateTrackingModal.module.scss'

interface CreateTrackingModalProps {
	open: boolean
	setOpen: Dispatch<SetStateAction<boolean>>
	fetchProducts: () => Promise<void>
}

export const CreateTrackingModal = ({
	open,
	setOpen,
	fetchProducts,
}: CreateTrackingModalProps) => {
	const [inputsData, setInputsData] = useState({ url: '' })
	const [isLoading, setIsLoading] = useState(false)
	const [tags, setTags] = useState<{ name: string }[]>([])

	const handleSubmit = async (e: React.SubmitEvent<HTMLFormElement>) => {
		e.preventDefault()
		if (!inputsData.url) {
			toast('Пожалуйста, заполните все поля', { type: 'error' })
			return
		}

		setIsLoading(true)
		try {
			const response: any = await cardsApi.addWatchItem(inputsData.url, tags)
			toast(response.message || 'Успешно добавлено')
			fetchProducts()
			setTimeout(fetchProducts, 8000)
			setTags([])
			setOpen(false)
		} catch (error: any) {
			const errorMessage =
				error.response?.data?.detail || 'Не удалось загрузить товары'
			toast.error(errorMessage)
		} finally {
			setIsLoading(false)
		}
	}

	const tagInput = useRef<HTMLInputElement>(null)

	const createTag = () => {
		if (
			tagInput.current!.value == '' ||
			tags.find(x => x.name == tagInput.current!.value)
		) {
			return
		}
		setTags([...tags, { name: tagInput.current!.value }])
		tagInput.current!.value = ''
		tagInput.current!.focus()
	}

	const deleteTag = (name: string) => {
		const filteredTags = tags.filter(x => x.name != name)
		setTags(filteredTags)
	}

	return (
		<Modal
			showCloseButton={false}
			isOpen={open}
			onClose={() => setOpen(false)}
			closeOnOverlayClick={false}
		>
			<div className={styles.modal}>
				<h3>Добавить товар</h3>

				<form onSubmit={handleSubmit}>
					<div className={styles.input_group}>
						<label htmlFor='url'>URL товара *</label>
						<Input
							id='url'
							type='url'
							placeholder='https://example.com/'
							onChange={el =>
								setInputsData({ ...inputsData, url: el.currentTarget.value })
							}
							disabled={isLoading}
							required
						/>
					</div>
					<div className={styles.input_group}>
						<label htmlFor='tags'>Теги</label>
						<div className={styles.tags_group}>
							<Input
								id='tags'
								type='text'
								ref={tagInput}
								disabled={isLoading}
							/>
							<Button type='light' onClick={createTag} disabled={isLoading}>
								Добавить
							</Button>
						</div>
						<div className={styles.tags_div}>
							{tags.map((el, index) => {
								return (
									<Badge className={styles.tag} key={index}>
										{el.name}
										<Button
											type='light'
											onClick={() => {
												deleteTag(el.name)
											}}
										>
											<DeleteIcon />
										</Button>
									</Badge>
								)
							})}
						</div>
					</div>
					<div className={styles.groupButtons}>
						<Button
							type='light'
							onClick={() => {
								setOpen(false)
								setTags([])
							}}
							disabled={isLoading}
						>
							Отмена
						</Button>
						<Button formType='submit' disabled={isLoading}>
							{isLoading ? 'Добавление товара...' : 'Добавить товар'}
						</Button>
					</div>
				</form>
			</div>
		</Modal>
	)
}

export default CreateTrackingModal
