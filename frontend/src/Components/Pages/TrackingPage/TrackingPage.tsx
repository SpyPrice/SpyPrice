import { cardsApi, type ItemStatistic } from '@/Api/trackingApi'
import Badge from '@/Components/UI/Badge'
import Button from '@/Components/UI/Button'
import Card from '@/Components/UI/Card'
import Table, { TableCell, TableHeader, TableRow } from '@/Components/UI/Table'
import { useTitle } from '@/Hooks'
import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { CartesianGrid, Line, LineChart, Tooltip, XAxis, YAxis } from 'recharts'
import styles from './TrackingPage.module.scss'

export const TrackingPage = () => {
	useTitle('Товар')
	const [item, setItem] = useState<ItemStatistic>()
	const [dataChart, setDataChart] = useState<any>()
	const { id } = useParams()

	useEffect(() => {
		fetchProducts()
	}, [])

	const fetchProducts = async () => {
		try {
			const data: any = await cardsApi.getCardInfo(+id!)
			setItem(data)
			setDataChart(
				data?.update_history.map((el: any) => {
					return {
						price: el.price,
						time: formatDateShort(el.time),
					}
				}),
			)
		} catch (error) {
			console.error('Failed to fetch item:', error)
		}
	}

	const formatDateShortTime = (dateString: string): string => {
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

		return `${day} ${month}`
	}

	return (
		<div className={styles.container}>
			<Link to={'/dashboard'}>
				<Button type='dark-no-back'>← Вернуться на главную</Button>
			</Link>
			<div className={styles.content}>
				<div className={styles.block}>
					<h2>{item?.item.name}</h2>
					{/* <div className={styles.buttons}>
            <Button>Редактировать</Button>
            <Button type='danger'>Удалить</Button>
          </div> */}
				</div>
				<div className={styles.badges}>
					<Badge type='main'>{item?.item.source.name}</Badge>
					{item?.item.tags.map(el => {
						return <Badge>{el.name}</Badge>
					})}
				</div>
				<a href={item?.item.url} target='_blank'>
					{item?.item.url}
				</a>
			</div>

			<Card className={styles.topCard}>
				<div className={styles.currentPrice}>
					<p className={styles.title}>Текущая цена</p>
					<p className={styles.currentPrice_value}>
						{item?.item.last_snapshot?.price} ₽
					</p>
				</div>
				<div className={styles.updatePrice}>
					<p className={styles.title}>Изменение за 7 дней</p>
					<div className={styles.updatePrice_value}>
						{item?.item.snapshot_7_days_ago != null ? (
							<Badge price='up'>{item?.item.snapshot_7_days_ago.price} ₽</Badge>
						) : (
							<Badge size='large'>-</Badge>
						)}
					</div>
				</div>
				<div className={styles.updatePrice30}>
					<p className={styles.title}>Изменение за 30 дней</p>
					<div className={styles.updatePrice30_value}>
						{item?.item.snapshot_7_days_ago != null ? (
							<Badge price='up'>{item?.item.snapshot_7_days_ago.price} ₽</Badge>
						) : (
							<Badge size='large'>-</Badge>
						)}
					</div>
				</div>
				<div className={styles.updatePriceDate}>
					<p className={styles.title}>Последнее обновление</p>
					<p className={styles.updatePriceDate_value}>
						{formatDateShortTime(item?.item.last_snapshot?.time!)}
					</p>
				</div>
			</Card>

			<Card className={styles.bottomCard}>
				<div>График цен</div>
				<LineChart className={styles.chart} responsive data={dataChart}>
					<CartesianGrid strokeDasharray='3 3' />
					<YAxis />
					<XAxis width='auto' dataKey='time' />
					<Tooltip />
					<Line type='monotone' dataKey='price' />
				</LineChart>
				<div className={styles.pricesBlock}>
					<div className={styles.minPrice}>
						<p className={styles.title}>Мин. цена</p>
						<p className={styles.price}>{item?.statistics.min_price.price} ₽</p>
					</div>
					<div className={styles.maxPrice}>
						<p className={styles.title}>Макс. цена</p>
						<p className={styles.price}>{item?.statistics.max_price.price} ₽</p>
					</div>
					<div className={styles.avgPrice}>
						<p className={styles.title}>Средняя цена</p>
						<p className={styles.price}>{item?.statistics.avg_price} ₽</p>
					</div>
				</div>
			</Card>

			<Card className={styles.bottomCard}>
				<div>История обновлений</div>

				<Table>
					<TableHeader>
						<TableCell>Дата и время</TableCell>
						<TableCell>Цена</TableCell>
					</TableHeader>
					{item?.update_history.map((el: any, index) => {
						return (
							<TableRow key={index}>
								<TableCell>{formatDateShortTime(el.time)}</TableCell>
								<TableCell>{el.price} ₽</TableCell>
							</TableRow>
						)
					})}
				</Table>
			</Card>
		</div>
	)
}

export default TrackingPage
