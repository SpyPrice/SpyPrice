import { cardsApi, type ItemStatistic } from '@/Api/trackingApi'
import Badge from '@/Components/UI/Badge'
import Button from '@/Components/UI/Button'
import Card from '@/Components/UI/Card'
import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import styles from './TrackingPage.module.scss'

export const TrackingPage = () => {
	const [data, setData] = useState<ItemStatistic>()
	const { id } = useParams()

	useEffect(() => {
		fetchProducts()
	}, [])

	const fetchProducts = async () => {
		try {
			const data: any = await cardsApi.getCardInfo(+id!)
			setData(data)
			console.log(data)
		} catch (error) {
			console.error('Failed to fetch item:', error)
		}
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
		const hours = date.getHours().toString().padStart(2, '0')
		const minutes = date.getMinutes().toString().padStart(2, '0')

		return `${day} ${month}, ${hours}:${minutes}`
	}

	return (
		<div className={styles.container}>
			<Button type='dark-no-back'>← Вернуться на главную</Button>
			<div className={styles.content}>
				<div className={styles.block}>
					<h2>{data?.item.name}</h2>
					{/* <div className={styles.buttons}>
            <Button>Редактировать</Button>
            <Button type='danger'>Удалить</Button>
          </div> */}
				</div>
				<div className={styles.badges}>
					<Badge type='main'>{data?.item.source.name}</Badge>
					{data?.item.tags.map(el => {
						return <Badge>{el.name}</Badge>
					})}
				</div>
				<a href={data?.item.url} target='_blank'>
					{data?.item.url}
				</a>
			</div>

			<Card className={styles.topCard}>
				<div className={styles.currentPrice}>
					<p className={styles.title}>Текущая цена</p>
					<p className={styles.currentPrice_value}>
						{data?.item.last_snapshot?.price} ₽
					</p>
				</div>
				<div className={styles.updatePrice}>
					<p className={styles.title}>Изменение за 7 дней</p>
					<div className={styles.updatePrice_value}>
						{data?.item.snapshot_7_days_ago != null ? (
							<Badge price='up'>{data?.item.snapshot_7_days_ago.price} ₽</Badge>
						) : (
							<Badge size='large'>-</Badge>
						)}
					</div>
				</div>
				<div className={styles.updatePrice30}>
					<p className={styles.title}>Изменение за 30 дней</p>
					<div className={styles.updatePrice30_value}>
						{data?.item.snapshot_7_days_ago != null ? (
							<Badge price='up'>15302 ₽</Badge>
						) : (
							<Badge size='large'>-</Badge>
						)}
					</div>
				</div>
				<div className={styles.updatePriceDate}>
					<p className={styles.title}>Последнее обновление</p>
					<p className={styles.updatePriceDate_value}>
						{formatDateShort(data?.item.last_snapshot?.time!)}
					</p>
				</div>
			</Card>

			<Card className={styles.bottomCard}>
				<div>График цен</div>
				<div className={styles.pricesBlock}>
					<div className={styles.minPrice}>
						<p className={styles.title}>Мин. цена</p>
						<p className={styles.price}>{data?.statistics.min_price.price} ₽</p>
					</div>
					<div className={styles.maxPrice}>
						<p className={styles.title}>Макс. цена</p>
						<p className={styles.price}>{data?.statistics.max_price.price} ₽</p>
					</div>
					<div className={styles.avgPrice}>
						<p className={styles.title}>Средняя цена</p>
						<p className={styles.price}>{data?.statistics.avg_price} ₽</p>
					</div>
				</div>
			</Card>
		</div>
	)
}

export default TrackingPage
