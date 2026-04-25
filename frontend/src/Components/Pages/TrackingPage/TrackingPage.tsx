import { cardsApi, type ItemStatistic } from '@/Api/trackingApi'
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
import { useTitle } from '@/Hooks'
import { useEffect, useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import { toast } from 'react-toastify'
import { CartesianGrid, Line, LineChart, Tooltip, XAxis, YAxis } from 'recharts'
import styles from './TrackingPage.module.scss'

export const TrackingPage = () => {
	useTitle('Товар')
	const [item, setItem] = useState<ItemStatistic>()
	const [dataChart, setDataChart] = useState<any>()
	const { id } = useParams()
	const navigate = useNavigate()

	useEffect(() => {
		fetchProducts()
	}, [])

	const fetchProducts = async () => {
		try {
			const data: any = await cardsApi.getCardInfo(+id!)

			setItem(data)

			const sortedHistory = data?.update_history.sort(
				(a: any, b: any) =>
					new Date(a.time).getTime() - new Date(b.time).getTime(),
			)

			const now = new Date()
			const thirtyDaysAgo = new Date()
			thirtyDaysAgo.setDate(now.getDate() - 30)

			const last30DaysHistory = sortedHistory?.filter((el: any) => {
				const itemDate = new Date(el.time)
				return itemDate >= thirtyDaysAgo
			})

			let chartData
			if (last30DaysHistory?.length > 20) {
				chartData = groupDataByDay(last30DaysHistory)
			} else {
				chartData = last30DaysHistory?.map((el: any) => {
					return {
						Цена: el.price,
						time: formatDateShort(el.time, false),
					}
				})
			}

			setDataChart(chartData)
		} catch (error) {
			console.error('Failed to fetch item:', error)
			navigate('/dashboard')
		}
	}

	const groupDataByDay = (history: any[]) => {
		const groupedByDate: {
			[key: string]: {
				price: number
				time: string
				fullDate: Date
				originalTime: Date
			}
		} = {}

		history.forEach((el: any) => {
			const dateKey = formatDateShort(el.time, false)
			const currentDate = new Date(el.time)

			if (
				!groupedByDate[dateKey] ||
				currentDate > groupedByDate[dateKey].originalTime
			) {
				groupedByDate[dateKey] = {
					price: el.price,
					time: el.time,
					fullDate: currentDate,
					originalTime: currentDate,
				}
			}
		})

		return Object.values(groupedByDate)
			.sort((a, b) => a.fullDate.getTime() - b.fullDate.getTime())
			.map(el => ({
				Цена: el.price,
				time: formatDateShort(el.time, false),
			}))
	}

	const formatDateShort = (
		dateString: string,
		time: boolean = false,
	): string => {
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

		return time ? `${day} ${month}, ${hours}:${minutes}` : `${day} ${month}`
	}

	const handleDelete = async () => {
		const response: any = await cardsApi.deleteCard(+id!)
		if (response.status == 'success') {
			navigate('/dashboard')
			toast.info('Удалено успешно!')
		} else {
			toast.error('Ошибка удаления!')
		}
	}

	return (
		<div className={styles.container}>
			<Link to={'/dashboard'}>
				<Button type='dark-no-back'>← Вернуться на главную</Button>
			</Link>
			<div className={styles.content}>
				<div className={styles.block}>
					<h2>{item?.item.name}</h2>
					<div className={styles.buttons}>
						{/* <Button>Редактировать</Button> */}
						<Button type='danger' onClick={handleDelete}>
							<DeleteIcon />
							Удалить
						</Button>
					</div>
				</div>
				<div className={styles.badges}>
					<Badge type='main'>{item?.item.source.name}</Badge>
					{item?.item.tags.map(el => {
						return <Badge key={el.id}>{el.name}</Badge>
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
							<Badge
								price={
									+item?.item.snapshot_7_days_ago.price <
									+item?.item.last_snapshot?.price!
										? 'down'
										: +item?.item.snapshot_7_days_ago.price >
											  +item?.item.last_snapshot?.price!
											? 'up'
											: 'equals'
								}
							>
								{item?.item.snapshot_7_days_ago.price} ₽
							</Badge>
						) : (
							<Badge size='large'>-</Badge>
						)}
					</div>
				</div>
				<div className={styles.updatePrice30}>
					<p className={styles.title}>Изменение за 30 дней</p>
					<div className={styles.updatePrice30_value}>
						{item?.item.snapshot_30_days_ago != null ? (
							<Badge
								price={
									+item?.item.snapshot_30_days_ago.price <
									+item?.item.last_snapshot?.price!
										? 'down'
										: +item?.item.snapshot_30_days_ago.price >
											  +item?.item.last_snapshot?.price!
											? 'up'
											: 'equals'
								}
							>
								{item?.item.snapshot_30_days_ago.price} ₽
							</Badge>
						) : (
							<Badge size='large'>-</Badge>
						)}
					</div>
				</div>
				<div className={styles.updatePriceDate}>
					<p className={styles.title}>Последнее обновление</p>
					<p className={styles.updatePriceDate_value}>
						{formatDateShort(item?.item.last_snapshot?.time!, true)}
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
					<Line type='monotone' dataKey='Цена' />
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
					<TableBody>
						{item?.update_history &&
							[...item.update_history].reverse().map((el: any, index) => {
								return (
									<TableRow key={index}>
										<TableCell>{formatDateShort(el.time, true)}</TableCell>
										<TableCell>{el.price} ₽</TableCell>
									</TableRow>
								)
							})}
					</TableBody>
				</Table>
			</Card>
		</div>
	)
}

export default TrackingPage
