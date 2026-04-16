import { useTitle } from '@Hooks/useTitle'
import { Link } from 'react-router-dom'
import styles from './NotFoundPage.module.scss'

export const NotFoundPage = () => {
	useTitle('404')

	return (
		<div className={styles.container}>
			<p>404</p>
			<Link to={'/'}>На главную</Link>
		</div>
	)
}

export default NotFoundPage
