import type { ItemRead } from '@/Api/trackingApi'
import Badge from '@/Components/UI/Badge'
import Table, { TableCell, TableHeader, TableRow } from '@/Components/UI/Table'
import { useNavigate } from 'react-router-dom'
import styles from './ProductTable.module.scss'

interface ProductTableProps {
	data: ItemRead[]
}

export const ProductTable = ({ data }: ProductTableProps) => {
	const navigate = useNavigate()

	const formatDateShort = (dateString: string): string => {
		const date = new Date(dateString)

		const months = [
			'янв.',
			'фев.',
			'мар.',
			'апр.',
			'мая',
			'июн.',
			'июл.',
			'авг.',
			'сен.',
			'окт.',
			'ноя.',
			'дек.',
		]

		const day = date.getDate()
		const month = months[date.getMonth()]
		const hours = date.getHours().toString().padStart(2, '0')
		const minutes = date.getMinutes().toString().padStart(2, '0')

		return `${day} ${month}, ${hours}:${minutes}`
	}

	return (
		<Table>
			<TableHeader>
				<TableCell>Товар</TableCell>
				<TableCell>Магазин</TableCell>
				<TableCell>Текущая цена</TableCell>
				<TableCell>За 7 дней</TableCell>
				<TableCell>За 30 дней</TableCell>
				<TableCell>Обновлено</TableCell>
			</TableHeader>
			{data.map(el => {
				return (
					<TableRow onClick={() => navigate(`/tracking/${el.id}`)}>
						<TableCell>
							<div className={styles.name}>
								<p>{el.name}</p>
								<div className={styles.badges}>
									{el.tags.map(el => {
										return <Badge>{el.name}</Badge>
									})}
								</div>
							</div>
						</TableCell>
						<TableCell>
							<Badge type='main'>{el.source.name}</Badge>
						</TableCell>
						<TableCell className={styles.price}>
							{el.last_snapshot?.price} ₽
						</TableCell>
						<TableCell>
							{el.snapshot_7_days_ago == null ? (
								<Badge size='large'>-</Badge>
							) : (
								el.snapshot_7_days_ago?.price
							)}
						</TableCell>
						<TableCell>
							{el.snapshot_7_days_ago == null ? (
								<Badge size='large'>-</Badge>
							) : (
								el.snapshot_7_days_ago?.price
							)}
						</TableCell>
						<TableCell>{formatDateShort(el.last_snapshot?.time!)}</TableCell>
					</TableRow>
				)
			})}
		</Table>
	)
}

export default ProductTable
