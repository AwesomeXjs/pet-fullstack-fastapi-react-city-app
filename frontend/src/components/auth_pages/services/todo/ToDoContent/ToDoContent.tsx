import { FC } from 'react'
import styles from './styles.module.scss'
import { useNavigate } from 'react-router-dom'

const ToDoContent: FC = () => {
	const navigate = useNavigate()

	return (
		<div className={styles.todoContentWrapper}>
			<div onClick={() => navigate('/createTodo')} className={styles.toDoCard}>
				<h1>CREATE TODO</h1>
			</div>
			<div onClick={() => navigate('/todoList')} className={styles.toDoCard}>
				<h1>MY TODO LIST</h1>
			</div>
		</div>
	)
}

export default ToDoContent
