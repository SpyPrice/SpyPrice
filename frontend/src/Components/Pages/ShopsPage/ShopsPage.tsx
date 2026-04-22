import Card from '@/Components/UI/Card'
import { useTitle } from '@/Hooks'
import styles from './ShopsPage.module.scss'

export const ShopsPage = () => {
	useTitle('Магазины')

	const sites = [
		{
			name: 'DNS',
			url: 'https://dns-shop.ru',
		},
		{
			name: 'Читай-город',
			url: 'https://www.chitai-gorod.ru',
		},
		{
			name: 'Steam',
			url: 'https://store.steampowered.com/',
		},
		{
			name: 'Steam market',
			url: 'https://steamcommunity.com/market',
		},
		{
			name: 'Ozon',
			url: 'https://www.ozon.ru',
		},
		{
			name: 'Aliexpress',
			url: 'https://aliexpress.ru',
		},
		{
			name: 'Авто.ру',
			url: 'https://auto.ru',
		},
		{
			name: 'Авито',
			url: 'https://www.avito.ru',
		},
		{
			name: 'Ситилинк',
			url: 'https://www.citilink.ru',
		},
		{
			name: 'GGsel',
			url: 'https://ggsel.net',
		},
		{
			name: 'Хоббигеймс',
			url: 'https://hobbygames.ru',
		},
		{
			name: 'LisSkins',
			url: 'https://lis-skins.com',
		},
		{
			name: 'Мосигра',
			url: 'https://www.mosigra.ru',
		},
		{
			name: 'М.Видео',
			url: 'https://www.mvideo.ru',
		},
		{
			name: 'Playerok',
			url: 'https://playerok.com',
		},
		{
			name: 'PROSTORE',
			url: 'https://prostore-protechno.ru',
		},
		{
			name: 'Яндекс Маркет',
			url: 'https://market.yandex.ru',
		},
	]

	return (
		<div className={styles.container}>
			<h2>Поддерживаемые магазины</h2>
			<p>Список магазинов, из которых можно отслеживать товары</p>

			<Card className={styles.warning}>
				<img src='/info.svg' alt='Предупреждение' />
				<p>
					На этапе MVP список магазинов фиксирован. Если нужный вам магазин
					отсутствует, свяжитесь с поддержкой для добавления нового источника.
				</p>
			</Card>

			<div className={styles.cards}>
				{sites.map((el, index) => {
					return (
						<Card key={index} className={styles.card}>
							<div className={styles.card_img}>
								<img src='/shop.svg' alt='Магазин' />
							</div>
							<div className={styles.card_content}>
								<h3>{el.name}</h3>
								<p>
									Сайт:
									<a href={el.url} target='_blank'>
										{el.url}
									</a>
								</p>
							</div>
						</Card>
					)
				})}
			</div>
		</div>
	)
}

export default ShopsPage
