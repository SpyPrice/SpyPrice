import { cardsApi, type ItemRead } from '@/Api/trackingApi'
import DeleteIcon from '@/Assets/delete.svg?react'
import Badge from '@/Components/UI/Badge'
import Button from '@/Components/UI/Button'
import Card from '@/Components/UI/Card'
import Table, {
	TableBody,
	TableCell,
	TableHeader,
	TableRow,
} from '@/Components/UI/Table'
import { useNavigate } from 'react-router-dom'
import { toast } from 'react-toastify'
import styles from './ProductTable.module.scss'

interface ProductTableProps {
	data: ItemRead[]
	fetchProducts: () => Promise<void>
}

export const ProductTable = ({ data, fetchProducts }: ProductTableProps) => {
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

	const handleDelete = async (id: number) => {
		const response: any = await cardsApi.deleteCard(id)
		if (response.status == 'success') {
			toast.info('Удалено успешно!')
			fetchProducts()
		} else {
			toast.error('Ошибка удаления!')
		}
	}

	return (
		<>
			<div className={styles.desktop_view}>
				<Table>
					<TableHeader>
						<TableCell>Товар</TableCell>
						<TableCell>Магазин</TableCell>
						<TableCell>Текущая цена</TableCell>
						<TableCell>За 7 дней</TableCell>
						<TableCell>За 30 дней</TableCell>
						<TableCell>Обновлено</TableCell>
					</TableHeader>
					<TableBody>
						{data.map(el => {
							return (
								<TableRow
									key={el.id}
									onClick={() => {
										if (el.last_snapshot != null) {
											navigate(`/tracking/${el.id}`)
										}
									}}
								>
									<TableCell>
										<div className={styles.name}>
											<p>{el.name}</p>
											<div className={styles.badges}>
												{el.tags.map(tag => {
													return <Badge key={tag.id}>{tag.name}</Badge>
												})}
											</div>
										</div>
									</TableCell>
									<TableCell>
										<Badge type='main'>{el.source.name}</Badge>
									</TableCell>
									<TableCell className={styles.price}>
										{el.last_snapshot?.price != null
											? `${el.last_snapshot?.price} ₽`
											: ''}
									</TableCell>
									<TableCell>
										{el.snapshot_7_days_ago == null ? (
											<Badge size='large'>-</Badge>
										) : (
											<Badge
												size='small'
												price={
													+el.snapshot_7_days_ago.price <
													+el.last_snapshot?.price!
														? 'down'
														: +el.snapshot_7_days_ago.price >
															  +el.last_snapshot?.price!
															? 'up'
															: 'equals'
												}
											>
												{el.snapshot_7_days_ago.price} ₽
											</Badge>
										)}
									</TableCell>
									<TableCell>
										{el.snapshot_30_days_ago == null ? (
											<Badge size='large'>-</Badge>
										) : (
											<Badge
												size='small'
												price={
													+el.snapshot_30_days_ago.price <
													+el.last_snapshot?.price!
														? 'down'
														: +el.snapshot_30_days_ago.price >
															  +el.last_snapshot?.price!
															? 'up'
															: 'equals'
												}
											>
												{el.snapshot_30_days_ago.price} ₽
											</Badge>
										)}
									</TableCell>
									<TableCell>
										{el.last_snapshot == null ? (
											<Button
												type='danger'
												size='small'
												onClick={() => handleDelete(el.id)}
											>
												<DeleteIcon />
												Удалить
											</Button>
										) : (
											formatDateShort(el.last_snapshot?.time!)
										)}
									</TableCell>
								</TableRow>
							)
						})}
					</TableBody>
				</Table>
			</div>
			<div className={styles.mobile_view}>
				<div className={styles.product_cards}>
					{data.map(el => {
						return (
							<Card
								key={el.id}
								className={styles.card}
								onClick={() => {
									if (el.last_snapshot != null) {
										navigate(`/tracking/${el.id}`)
									}
								}}
							>
								<p className={styles.name}>{el.name}</p>
								<div className={styles.badges}>
									<Badge type='main'>{el.source.name}</Badge>
									{el.tags.map(tag => {
										return <Badge>{tag.name}</Badge>
									})}
								</div>
								{el.last_snapshot == null ? (
									<div className={styles.deleteButton}>
										<Button
											type='danger'
											size='small'
											onClick={() => handleDelete(el.id)}
										>
											<DeleteIcon />
											Удалить
										</Button>
									</div>
								) : (
									<div className={styles.card__bottom}>
										<div>
											<p>Текущая цена:</p>
											<p className={styles.price}>
												{el.last_snapshot?.price != null ? (
													`${el.last_snapshot?.price} ₽`
												) : (
													<Badge>-</Badge>
												)}
											</p>
										</div>
										<div>
											<p>Последнее обновление:</p>
											{formatDateShort(el.last_snapshot.time)}
										</div>
									</div>
								)}
							</Card>
						)
					})}
				</div>
			</div>
		</>
	)
}

export default ProductTable
