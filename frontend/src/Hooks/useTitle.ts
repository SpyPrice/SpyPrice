import { useEffect } from 'react'

export const useTitle = (title: string) => {
	useEffect(() => {
		const fullTitle = title ? title : 'SpyPrice'
		document.title = fullTitle

		return () => {
			document.title = 'SpyPrice'
		}
	}, [title])
}
