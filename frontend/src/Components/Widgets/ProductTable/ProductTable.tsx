import Table, { TableCell, TableHeader, TableRow } from '@/Components/UI/Table'

interface ProductTableProps {
	data: any
}

export const ProductTable = ({ data }: ProductTableProps) => {
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
			<TableRow>
				<TableCell></TableCell>
				<TableCell></TableCell>
				<TableCell></TableCell>
				<TableCell></TableCell>
				<TableCell></TableCell>
				<TableCell></TableCell>
			</TableRow>
		</Table>
	)
}

export default ProductTable
