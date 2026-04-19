import { cardsApi, type ItemRead } from '@/Api/trackingApi'
import Button from '@/Components/UI/Button'
import Filter from '@/Components/Widgets/Filter'
import ProductTable from '@/Components/Widgets/ProductTable'
import { useEffect, useState } from 'react'
import styles from './DashboardPage.module.scss'

const getProductText = (count: number): string => {
	if (count === 0) return 'товаров'
	if (count === 1) return 'товар'
	if (count >= 2 && count <= 4) return 'товара'
	return 'товаров'
}

export const DashboardPage = () => {
	const [products, setProducts] = useState<ItemRead[]>([])

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

	return (
		<div className={styles.container}>
			<h2>Отслеживаемые товары</h2>
			<div className={styles.block}>
				<p>
					{products.length} {getProductText(products.length)}
				</p>
				<Button>Добавить товар</Button>
			</div>

			<Filter />

			<ProductTable data={''} />
		</div>
	)
}

export default DashboardPage
