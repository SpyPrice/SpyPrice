import Button from '@/Components/UI/Button'
import Filter from '@/Components/Widgets/Filter'
import ProductTable from '@/Components/Widgets/ProductTable'
import styles from './DashboardPage.module.scss'

export const DashboardPage = () => {
	return (
		<div className={styles.container}>
			<h2>Отслеживаемые товары</h2>
			<div className={styles.block}>
				<p>5 товаров</p>
				<Button>Добавить товар</Button>
			</div>

			<Filter />

			<ProductTable data={''} />
		</div>
	)
}

export default DashboardPage
