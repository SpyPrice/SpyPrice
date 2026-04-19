import { cardsApi, type ItemRead } from '@/Api/trackingApi'
import Button from '@/Components/UI/Button'
import Input from '@/Components/UI/Input'
import Modal from '@/Components/UI/Modal'
import ProductTable from '@/Components/Widgets/ProductTable'
import { useEffect, useState } from 'react'
import { toast } from 'react-toastify'
import styles from './DashboardPage.module.scss'

const getProductText = (count: number): string => {
	if (count === 0) return 'товаров'
	if (count === 1) return 'товар'
	if (count >= 2 && count <= 4) return 'товара'
	return 'товаров'
}

export const DashboardPage = () => {
	const [isModalOpen, setIsModalOpen] = useState(false)
	const [products, setProducts] = useState<ItemRead[]>([])
	const [inputsData, setInputsData] = useState({ url: '' })
	const [isLoading, setIsLoading] = useState(false)

	useEffect(() => {
		fetchProducts()
	}, [])

	const fetchProducts = async () => {
		try {
			const data: any = await cardsApi.getAllWatchItems()
			setProducts(data)
			console.log(data)
		} catch (error) {
			console.error('Failed to fetch products:', error)
		}
	}

	const handleSubmit = async (e: React.SubmitEvent<HTMLFormElement>) => {
		e.preventDefault()
		if (!inputsData.url) {
			toast('Пожалуйста, заполните все поля', { type: 'error' })
			return
		}

		setIsLoading(true)
		try {
			await cardsApi.addWatchItem(inputsData.url)
			toast('Успешно добавлено')
			setTimeout(fetchProducts, 8000)
			setIsModalOpen(false)
		} catch (error: any) {
			const errorMessage =
				error.response?.data?.detail || 'Не удалось загрузить товары'
			toast.error(errorMessage)
		} finally {
			setIsLoading(false)
		}
	}

	return (
		<>
			<div className={styles.container}>
				<h2>Отслеживаемые товары</h2>
				<div className={styles.block}>
					<p>
						{products.length} {getProductText(products.length)}
					</p>
					<Button onClick={() => setIsModalOpen(true)}>Добавить товар</Button>
				</div>

				{/* <Filter /> */}

				<ProductTable data={products} />
			</div>

			<Modal
				showCloseButton={false}
				isOpen={isModalOpen}
				onClose={() => setIsModalOpen(false)}
				closeOnOverlayClick={false}
			>
				<div className={styles.modal}>
					<h3>Добавить товар</h3>
					<p>
						Вставьте ссылку на товар и выберите магазин для отслеживания цены
					</p>

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
								required
							/>
						</div>
						<div className={styles.groupButtons}>
							<Button
								type='light'
								onClick={() => setIsModalOpen(false)}
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
		</>
	)
}

export default DashboardPage
