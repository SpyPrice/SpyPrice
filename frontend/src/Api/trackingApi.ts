import api from './axios'

export interface ItemCreate {
	source_url: string
}

export interface WatchResponse {
	status: 'success' | 'pending'
	message: string
}

export interface LastSnapshot {
	price: string
	time: string
}

export interface Source {
	id: number
	name: string
}

export interface Tag {
	id: number
	name: string
}

export interface ItemRead {
	id: number
	name: string
	url: string
	is_in_stock: boolean
	currency: string
	last_snapshot: LastSnapshot | null
	snapshot_7_days_ago: LastSnapshot | null
	source: Source
	tags: Tag[]
}

export interface ItemReadExtended extends ItemRead {
	source_url: string
	created_at: string
	last_price?: number
	last_check?: string
}

export interface PriceSnapshot {
	id: number
	price: number
	created_at: string
}

export interface PriceStatistics {
	min_price: LastSnapshot
	max_price: LastSnapshot
	avg_price: number
}

export interface ItemStatistic {
	item: ItemRead
	statistics: PriceStatistics
	update_history: PriceSnapshot[]
}

export const cardsApi = {
	addWatchItem: (sourceUrl: string) =>
		api.post<WatchResponse>('/cards/add_watch_item', { source_url: sourceUrl }),

	getAllWatchItems: () => api.get<ItemRead[]>('/cards/get_all_watch_items'),

	getCardInfo: (cardId: number) =>
		api.get<ItemStatistic>(`/cards/card_info?card_id=${cardId}`),
}
