import { FC } from 'react'

import styles from './styles.module.scss'
import Todo from './services/todo/Todo'

interface AuthPageProps {}

const AuthPage: FC<AuthPageProps> = () => {
	return (
		<div className={`${styles.mainPageContent} container`}>
			<Todo />
		</div>
	)
}

export default AuthPage
