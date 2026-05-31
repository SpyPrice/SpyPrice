import { cardsApi, type ItemRead } from '@/Api/trackingApi'
import Button from '@/Components/UI/Button'
import CreateTrackingModal from '@/Components/Widgets/CreateTrackingModal'
import Filter from '@/Components/Widgets/Filter'
import ProductTable from '@/Components/Widgets/ProductTable'
import { useTitle } from '@/Hooks'
import { useEffect, useState } from 'react'
import styles from './DashboardPage.module.scss'

const getProductText = (count: number): string => {
	if (count === 0) return 'товаров'
	if (count === 1) return 'товар'
	if (count >= 2 && count <= 4) return 'товара'
	return 'товаров'
}

export const DashboardPage = () => {
	useTitle('Товары')

	const [isModalOpen, setIsModalOpen] = useState(false)
	const [originalProducts, setOriginalProducts] = useState<ItemRead[]>([])
	const [filteredProducts, setFilteredProducts] = useState<ItemRead[]>([])

	useEffect(() => {
		fetchProducts()
		const timer = setInterval(fetchProducts, 15000)
		timer
	}, [])

	const fetchProducts = async () => {
		try {
			const data: any = await cardsApi.getAllWatchItems()
			setOriginalProducts(data)
			setFilteredProducts(data)
		} catch (error) {
			console.error('Failed to fetch products:', error)
		}
	}

	return (
		<>
			<div className={styles.container}>
				<h2>Отслеживаемые товары</h2>
				<div className={styles.block}>
					<p>
						{filteredProducts.length} {getProductText(filteredProducts.length)}
					</p>
					<Button onClick={() => setIsModalOpen(true)}>
						<img src='/plus.svg' alt='Плюс' />
						<p>Добавить товар</p>
					</Button>
				</div>

				<Filter
					setFilteredProducts={setFilteredProducts}
					originalProducts={originalProducts}
				/>

				<ProductTable
					data={[...filteredProducts].reverse()}
					fetchProducts={fetchProducts}
				/>

				<CreateTrackingModal
					open={isModalOpen}
					setOpen={setIsModalOpen}
					fetchProducts={fetchProducts}
				/>
			</div>
		</>
	)
}

export default DashboardPage
