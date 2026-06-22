import ShopIcon from '@/Assets/shop.svg?react'
import Card from '@/Components/UI/Card'
import { useTitle } from '@/Hooks'
import styles from './ShopsPage.module.scss'

export const ShopsPage = () => {
	useTitle('Магазины')

	const sites = [
		{
			name: 'DNS',
			url: 'https://dns-shop.ru',
			logo: '/shops_icon/dns.png',
		},
		{
			name: 'Читай-город',
			url: 'https://www.chitai-gorod.ru',
			logo: '/shops_icon/readcity.jpg',
		},
		{
			name: 'Steam',
			url: 'https://store.steampowered.com',
			logo: '/shops_icon/steam.png',
		},
		{
			name: 'Steam market',
			url: 'https://steamcommunity.com/market',
			logo: '/shops_icon/steam.png',
		},
		{
			name: 'Ozon',
			url: 'https://www.ozon.ru',
			logo: '/shops_icon/ozon.png',
		},
		{
			name: 'Aliexpress',
			url: 'https://aliexpress.ru',
			logo: '/shops_icon/aliexpress.png',
		},
		{
			name: 'Авто.ру',
			url: 'https://auto.ru',
			logo: '/shops_icon/avtoru.png',
		},
		{
			name: 'Авито',
			url: 'https://www.avito.ru',
			logo: '/shops_icon/avito.png',
		},
		{
			name: 'Ситилинк',
			url: 'https://www.citilink.ru',
			logo: '/shops_icon/sitilink.jpg',
		},
		{
			name: 'GGsel',
			url: 'https://ggsel.net',
			logo: '/shops_icon/ggsel.png',
		},
		{
			name: 'Хоббигеймс',
			url: 'https://hobbygames.ru',
			logo: '/shops_icon/hg.png',
		},
		{
			name: 'LisSkins',
			url: 'https://lis-skins.com',
			logo: '/shops_icon/lis.svg',
		},
		{
			name: 'Мосигра',
			url: 'https://www.mosigra.ru',
			logo: '/shops_icon/mosigra.png',
		},
		{
			name: 'М.Видео',
			url: 'https://www.mvideo.ru',
			logo: '/shops_icon/mvideo.webp',
		},
		{
			name: 'Playerok',
			url: 'https://playerok.com',
			logo: '/shops_icon/playerok.webp',
		},
		{
			name: 'PROSTORE',
			url: 'https://prostore-protechno.ru',
			logo: '/shops_icon/prostore.svg',
		},
		{
			name: 'Яндекс Маркет',
			url: 'https://market.yandex.ru',
			logo: '/shops_icon/YaMarket.webp',
		},
	]

	return (
		<div className={styles.container}>
			<h2>Поддерживаемые магазины</h2>
			<p>Список магазинов, из которых можно отслеживать товары</p>

			<div className={styles.cards}>
				{sites.map((el, index) => {
					return (
						<Card key={index} className={styles.card}>
							<div className={styles.card_img}>
								{el.logo == null ? (
									<ShopIcon />
								) : (
									<img src={el.logo} alt={el.name} />
								)}
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
