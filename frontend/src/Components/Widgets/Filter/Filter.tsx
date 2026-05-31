import type { ItemRead } from '@/Api/trackingApi'
import FilterIcon from '@/Assets/filter.svg?react'
import SearchIcon from '@/Assets/search.svg?react'
import Badge from '@/Components/UI/Badge'
import Button from '@/Components/UI/Button'
import Card from '@/Components/UI/Card'
import Input from '@/Components/UI/Input'
import Select from '@/Components/UI/Select'
import {
	useEffect,
	useMemo,
	useRef,
	useState,
	type Dispatch,
	type SetStateAction,
} from 'react'
import styles from './Filter.module.scss'

interface FilterProps {
	setFilteredProducts: Dispatch<SetStateAction<ItemRead[]>>
	originalProducts: ItemRead[]
}

export const Filter = ({
	setFilteredProducts,
	originalProducts,
}: FilterProps) => {
	const [search, useSearch] = useState('')
	const [selectedShop, setSelectedShop] = useState<string>('all')
	const [selectedTags, setSelectedTags] = useState<Set<string>>(new Set())
	const [showAllTags, setShowAllTags] = useState(false)
	const tagsPopupRef = useRef<HTMLDivElement>(null)

	const shops = useMemo(() => {
		const uniqueShops = new Set(
			originalProducts.map(product => product.source?.name).filter(Boolean),
		)
		return ['all', ...Array.from(uniqueShops)]
	}, [originalProducts])

	const allTags = useMemo(() => {
		const uniqueTags = new Set<string>()

		originalProducts.forEach(product => {
			product.tags?.forEach(tag => {
				if (tag.name) {
					uniqueTags.add(tag.name)
				}
			})
		})

		return Array.from(uniqueTags)
	}, [originalProducts])

	const visibleTags = useMemo(() => {
		return allTags.slice(0, 5)
	}, [allTags])

	const sortedTags = useMemo(() => {
		const selected = Array.from(selectedTags)
		const notSelected = allTags.filter(tag => !selectedTags.has(tag))
		return [...selected, ...notSelected]
	}, [allTags, selectedTags])

	useEffect(() => {
		const handleClickOutside = (event: MouseEvent) => {
			if (
				tagsPopupRef.current &&
				!tagsPopupRef.current.contains(event.target as Node)
			) {
				setShowAllTags(false)
			}
		}
		document.addEventListener('mousedown', handleClickOutside)
		return () => document.removeEventListener('mousedown', handleClickOutside)
	}, [])

	const handleTagToggle = (tag: string) => {
		const newSelectedTags = new Set(selectedTags)
		if (newSelectedTags.has(tag)) {
			newSelectedTags.delete(tag)
		} else {
			newSelectedTags.add(tag)
		}
		setSelectedTags(newSelectedTags)
	}

	useEffect(() => {
		let filtered = [...originalProducts]

		if (search.trim()) {
			filtered = filtered.filter(product =>
				product.name.toLowerCase().includes(search.toLowerCase()),
			)
		}

		if (selectedShop !== 'all') {
			filtered = filtered.filter(
				product => product.source?.name === selectedShop,
			)
		}

		if (selectedTags.size > 0) {
			filtered = filtered.filter(product =>
				Array.from(selectedTags).every(selectedTag =>
					product.tags?.some(tag => tag.name === selectedTag),
				),
			)
		}

		setFilteredProducts(filtered)
	}, [
		search,
		selectedShop,
		selectedTags,
		originalProducts,
		setFilteredProducts,
	])

	const handleClearTags = () => {
		setSelectedTags(new Set())
	}

	return (
		<Card className={styles.card}>
			<label className={styles.label} htmlFor='search'>
				<SearchIcon />
				<Input
					onChange={e => useSearch(e.currentTarget.value)}
					id='search'
					placeholder='Поиск по названию'
				/>
			</label>
			<Select
				value={selectedShop}
				onChange={setSelectedShop}
				options={shops.map(shop => ({
					value: shop,
					label: shop === 'all' ? 'Все магазины' : shop,
				}))}
				placeholder='Выберите магазин'
			/>
			<div className={styles.tagsBlock}>
				<FilterIcon />
				<div className={styles.tags}>
					{visibleTags.map(tag => (
						<Badge
							key={tag}
							type={selectedTags.has(tag) ? 'main' : 'second'}
							onClick={() => handleTagToggle(tag)}
						>
							{tag}
						</Badge>
					))}
					{allTags.length > 5 && (
						<Badge onClick={() => setShowAllTags(!showAllTags)}>...</Badge>
					)}
				</div>
				{selectedTags.size > 0 && (
					<Button className={styles.clearButton} onClick={handleClearTags}>
						Очистить теги
					</Button>
				)}
			</div>

			{showAllTags && (
				<div className={styles.tagsPopup} ref={tagsPopupRef}>
					<div className={styles.tagsPopupHeader}>
						<span>Все теги</span>
						<button onClick={() => setShowAllTags(false)}>✕</button>
					</div>
					<div className={styles.tagsPopupContent}>
						{sortedTags.map(tag => (
							<Badge
								key={tag}
								type={selectedTags.has(tag) ? 'main' : 'second'}
								onClick={() => handleTagToggle(tag)}
							>
								{tag}
							</Badge>
						))}
					</div>
				</div>
			)}
		</Card>
	)
}

export default Filter
